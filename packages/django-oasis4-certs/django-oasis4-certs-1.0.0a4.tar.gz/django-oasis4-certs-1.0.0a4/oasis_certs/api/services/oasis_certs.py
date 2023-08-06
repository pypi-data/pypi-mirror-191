# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         26/01/23 9:40 PM
# Project:      CFHL Transactional Backend
# Module Name:  oasis_certs
# Description:
# ****************************************************************
from datetime import date
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError as CoreValidationError
from django.utils.translation import gettext_lazy as _
from oasis.models import Cycle
from oasis.models import Company
from oasis.models import Periods
from oasis_certs.lib.choices import CycleType
from oasis_certs.lib.cursors import Cursor
from oasis_certs.api.serializers import CertificateSerializer
from oasis_certs.models import Certificate
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.models import TokenUser
from wsgiref.util import FileWrapper
from zibanu.django.repository.lib.utils import DocumentGenerator
from zibanu.django.rest_framework.exceptions import APIException
from zibanu.django.rest_framework.exceptions import ValidationError
from zibanu.django.rest_framework.viewsets import ViewSet
from zibanu.django.utils import CodeGenerator
from zibanu.django.utils import ErrorMessages


class OasisCertsServices(ViewSet):
    __prefix = "oasis_certs"
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    if settings.DEBUG:
        authentication_classes.append(authentication.TokenAuthentication)

    def list_documents(self, request) -> Response:
        try:
            # If user is from simplejwt
            if isinstance(request.user, TokenUser):
                request.user = get_user_model().objects.get(pk=request.user.id)
            user = request.user

            if not hasattr(user, "profile"):
                raise ValidationError(_("The user is not registered."))

            if "category" in request.data.keys():
                qs = Certificate.objects.get_by_category(request.data.get("category"), user.profile.type)
                serializer = CertificateSerializer(instance=qs, many=True)
                data_return = []
                for data_record in serializer.data:
                    cycle_type = data_record.pop("cycle_type")
                    years = []
                    cycles = []
                    if cycle_type != CycleType.NONE:
                        qs_cycle = Cycle.objects.get_by_type(cycle_type=cycle_type)
                        for cycle in qs_cycle.all():
                            if cycle.get("year") not in years:
                                years.append(cycle.get("year"))

                            if cycle.get("cycle") not in cycles:
                                cycles.append(cycle.get("cycle"))

                    data_return.append(
                        {
                            "id": data_record.get("id"),
                            "name": data_record.get("name"),
                            "years": years,
                            "cycles": cycles
                        }
                    )
                status_return = status.HTTP_200_OK if len(data_return) > 0 else status.HTTP_204_NO_CONTENT
            else:
                raise ValidationError(ErrorMessages.DATA_REQUEST_NOT_FOUND,
                                      _("The 'category' parameter not found at request."))
        except Exception as exc:
            pass
        else:
            return Response(status=status_return, data=data_return)

    def gen_document(self, request) -> Response:
        """
        REST Service to generate a document based on key
        :param request: request object from HTTP Post.
        :return: response with status 200 if successfully
        """
        try:
            # Get today and default company
            today = date.today()
            default_company = settings.OASIS_DEFAULT_COMPANY
            company_data = Company.objects.get_by_company_id(default_company).first()

            # If user is from simplejwt
            if isinstance(request.user, TokenUser):
                request.user = get_user_model().objects.get(pk=request.user.id)
            user = request.user

            if not hasattr(request.user, "profile"):
                raise ValidationError(_("The user is not registered."), code=status.HTTP_401_UNAUTHORIZED)

            # Set year and period
            if {"year", "id", "cycle"} <= request.data.keys():
                cert_id = request.data.get("id")
                year = request.data.get("year")
                cycle = request.data.get("cycle")

                certificate = Certificate.objects.get(pk=cert_id)
                period = Cycle.objects.get_period(year, cycle, certificate.cycle_type)

                # Validate period status
                if certificate.closed:
                    if Periods.objects.is_open(year, period):
                        raise ValidationError(_("The period is not closed."))

                doc_data = Cursor.generate_document(certificate.query_text, user.profile.document_id, year, period)
                if len(doc_data) > 0:
                    # Determine issue_date
                    if certificate.issue_date is None:
                        certificate.issue_date = today
                    else:
                        issue_date = date(year, certificate.issue_date.month, certificate.issue_date.day)
                        certificate.issue_date = today if today <= issue_date else issue_date

                    # Determine template and template vars
                    template_name = certificate.template
                    generator = CodeGenerator("generate_pdf", code_length=10)
                    template_context = {
                        "company": company_data,
                        "user": user,
                        "certificate": certificate,
                        "doc_data": doc_data,
                        "year": year,
                        "period": period,
                        "code": generator.get_alpha_numeric_code()
                    }

                    document = DocumentGenerator(self.__prefix)
                    data_return = {
                        "file_id": document.generate_from_template(template_name, template_context, request,
                                                                   certificate.name)
                    }
                else:
                    raise ValidationError(_("User does not have data for this document."))
            else:
                raise ValidationError(_("Some json field required not found"))
        except Certificate.DoesNotExist:
            raise APIException(msg=ErrorMessages.NOT_FOUND, error=_("Certificate key does not exist."),
                               http_status=status.HTTP_404_NOT_FOUND)
        except Company.DoesNotExist:
            raise APIException(msg=ErrorMessages.NOT_FOUND, error=_("Company does not found"),
                               http_status=status.HTTP_404_NOT_FOUND)
        except CoreValidationError as exc:
            raise APIException(msg=ErrorMessages.DATA_REQUIRED, error=exc.message) from exc
        except ValidationError as exc:
            raise APIException(msg=ErrorMessages.NOT_FOUND, error=exc.detail[0]) from exc
        except Exception as exc:
            raise APIException(msg=ErrorMessages.NOT_CONTROLLED, error=str(exc)) from exc
        else:
            return Response(status=status.HTTP_200_OK, data=data_return)

    def get_document(self, request) -> Response:
        """
        REST service that return a pdf from document repository
        :param request: request object from HTTP
        :return: reponse with application/pdf document
        """
        try:
            # If user is from simplejwt
            if isinstance(request.user, TokenUser):
                request.user = get_user_model().objects.get(pk=request.user.id)

            user = request.user
            if "file_id" in request.data.keys():
                download_file = str(user.profile.document_id) + ".pdf"
                document = DocumentGenerator(self.__prefix)
                document_file = document.get_file(user=request.user, uuid=request.data.get("file_id"))
                file_handler = open(document_file, "rb")
                file_wrapper = FileWrapper(file_handler)
                response = Response(
                    headers={"Content-Disposition": f'attachment; filename={download_file}'},
                    content_type="application/pdf",
                )
                response.content = file_handler.read()
                file_handler.close()
            else:
                raise CoreValidationError(_("Field 'file_id' is required"))
        except ValueError as exc:
            raise APIException(msg=_("Data value error"), error=str(exc),
                               http_status=status.HTTP_412_PRECONDITION_FAILED) from exc
        except CoreValidationError as exc:
            raise APIException(msg=_("Data validation error"), error=exc.message,
                               http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except OSError as exc:
            raise APIException(msg=_("Document error"), error=exc.strerror,
                               http_status=status.HTTP_400_BAD_REQUEST) from exc
        except ObjectDoesNotExist as exc:
            raise APIException(msg=_("Document does not exists."), error=str(exc)) from exc
        else:
            return response
