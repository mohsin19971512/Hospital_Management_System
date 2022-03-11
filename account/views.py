from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from ninja import Router

from account.authorization import GlobalAuth, get_tokens_for_user
from account.schemas import AccountCreate, AuthOut, ContactSchema, SigninSchema, AccountOut, AccountUpdate, ChangePasswordSchema
from config.utils.schemas import MessageOut
from hospital.models import OutPatients
from hospital.schemas.patientSchema import PatientProfileSchemaIn
from hospital.models import Contact
User = get_user_model()

account_controller = Router(tags=['auth'])


@account_controller.post('signup', response={
    400: MessageOut,
    201: AuthOut,
})
def signup(request, account_in: AccountCreate):
    if account_in.password1 != account_in.password2:
        return 400, {'message': 'Passwords do not match!'}

    try:
        User.objects.get(email=account_in.email)
    except User.DoesNotExist:
        new_user = User.objects.create_user(
            first_name=account_in.first_name,
            last_name=account_in.last_name,
            phone_number = account_in.phone_number,
            email=account_in.email,
            password=account_in.password1,
            type = "patient"
        )
        new_user.save()
        type = new_user.type
        token = get_tokens_for_user(new_user)

        return 201, {
            'token': token,
            'account': new_user,
            'type' :type
        }

    return 400, {'message': 'User already registered!'}


@account_controller.post('signin', response={
    200: AuthOut,
    404: MessageOut,
})
def signin(request, signin_in: SigninSchema):
    user = authenticate(email=signin_in.email, password=signin_in.password)

    if not user:
        return 404, {'message': 'User does not exist'}
    type = user.type
    token = get_tokens_for_user(user)

    return {
        'token': token,
        'account': user,
        'type':type
    }



@account_controller.get('', auth=GlobalAuth(), response=AccountOut)
def me(request):
    return get_object_or_404(User, id=request.auth['pk'])


@account_controller.put('', auth=GlobalAuth(), response={
    200: AccountOut,

})
def update_account(request, update_in: AccountUpdate):
    User.objects.filter(id=request.auth['pk']).update(**update_in.dict())
    return get_object_or_404(User, id=request.auth['pk'])


@account_controller.post('change-password', auth=GlobalAuth(), response={
    200: MessageOut,
    400: MessageOut
})
def change_password(request, password_update_in: ChangePasswordSchema):
    # user = authenticate(get_object_or_404(User, id=request.auth['pk']).email, password_update_in.old_password)
    if password_update_in.new_password1 != password_update_in.new_password2:
        return 400, {'message': 'passwords do not match'}
    user = get_object_or_404(User, id=request.auth['pk'])
    is_it_him = user.check_password(password_update_in.old_password)

    if not is_it_him:
        return 400, {'message': 'Dude, make sure you are him!'}

    user.set_password(password_update_in.new_password1)
    user.save()
    return {'message': 'password updated successfully'}


@account_controller.post('contact-us', response={
    200: MessageOut,
})
def createContactUs(request, contact_in: ContactSchema):
    contact = Contact.objects.create(**contact_in.dict())
    contact.save()

    return 200,{"message":"Contact created successfully"}