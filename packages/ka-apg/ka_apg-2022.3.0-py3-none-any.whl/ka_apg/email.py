# coding=utf-8

from email_validator import validate_email, EmailNotValidError
# from verify_email import verify_email

# from munch import munchify

from typing import NewType
from typing import Dict, List, Union

AoD = NewType('AoD', List[Dict])
Value = NewType('Value', Union[str, List, Dict])


class Email:
    """ Manage Email
    """
    @staticmethod
    def verify(email):
        """ Verify email
        """
        # Log.Eq.debug(">>> email", email))
        # is_valid = verify_email(email, debug=True)
        # Log.Eq.debug(">>> is_valid", is_valid))
        # return is_valid
        return True

    @staticmethod
    def normalize(email):
        """ Normalize email
        """
        try:
            # Validate.
            valid = validate_email(
                      email, allow_smtputf8=True, check_deliverability=False)
            # Update with the normalized form.
            return valid.email
        except EmailNotValidError:
            # email is not valid, exception message is human-readable
            return email

    @classmethod
    def sh_d_email(cls, email):
        """ Show email as dictionary
        """
        email = email.strip().lower()

        a_email = email.split('@')
        user_name = a_email[0]
        host_name = a_email[1]

        a_user_name = user_name.split('.')
        a_host_name = host_name.split('.')

        # everything but the last element
        firstname = ' '.join(a_user_name[:-1])
        lastname = ' '.join(a_user_name[-1:])
        company = a_host_name[0]
        fullname = ' '.join(a_user_name)

        dic = {}
        dic['email'] = email
        dic['firstname'] = firstname
        dic['lastname'] = lastname
        dic['fullname'] = fullname
        dic['company'] = company
        dic['person'] = f"{fullname} {company}"
        dic['valid'] = cls.verify(email)

        return dic
