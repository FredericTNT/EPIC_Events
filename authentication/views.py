from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator as MailToken
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from authentication.serializers import RegisterSerializer, UserSerializer, UpdateUsersGroupsSerializer
from authentication.forms import SignUpForm
from authentication.models import User


class SignUpView(View):
    form_class = SignUpForm
    template_name = 'authentication/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MyLittleCompany Account'
            message = render_to_string('authentication/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': MailToken().make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, "Merci de cliquer sur le lien envoyé par email pour activer votre compte")

            return redirect('login-view')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and MailToken().check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            messages.success(request, "Confirmation email OK, votre compte est maintenant actif")
            return redirect('login-view')
        else:
            messages.warning(request, "Le lien de confirmation email est invalide (trop ancien ou déjà utilisé)")
            return redirect('login-view')


class SignUp(APIView):
    """ Enregistrer un utilisateur """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    """ Liste paginée de tous les utilisateurs (GET) """

    permission_classes = [IsAuthenticated, IsAdminUser]
    paginator = LimitOffsetPagination()

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        page = self.paginator.paginate_queryset(users, request, view=self)
        if page is not None:
            serializer = self.paginator.get_paginated_response(UserSerializer(page, many=True).data)
        else:
            serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetail(APIView):
    """ Modification du groupe de l'utilisateur (PUT) et suppression (DELETE) d'un utilisateur """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        user = get_object_or_404(User, id=self.kwargs['id_user'])
        self.check_object_permissions(self.request, user)
        return user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UpdateUsersGroupsSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        data = {'delete': 'ok'}
        return Response(data, status=status.HTTP_202_ACCEPTED)
