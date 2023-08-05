'''
This module by default deploys a configurable Identity Provider with a default Cognito User Pool. These resources can be used by your website to restrict access to only authenticated users if needed. All settings are configurable and the creation of these AuthN resources can be disabled if needed or configured to use custom AuthN providers i.e. Facebook, Google, etc.

Below is a conceptual view of the default architecture this module creates:

```
Cognito User Pool --------------------> Identity Pool
     |_ User Pool Client                     |_ Unauthenticated IAM Role
                                             |_ Authenticated IAM Role
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_cognito as _aws_cdk_aws_cognito_ceddda9d
import aws_cdk.aws_cognito_identitypool_alpha as _aws_cdk_aws_cognito_identitypool_alpha_e0ee7798
import constructs as _constructs_77d1e7e8


class UserIdentity(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/identity.UserIdentity",
):
    '''(experimental) Creates an Identity Pool with sane defaults configured.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        identity_pool_options: typing.Optional[typing.Union[_aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPoolProps, typing.Dict[builtins.str, typing.Any]]] = None,
        user_pool: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param identity_pool_options: (experimental) Configuration for the Identity Pool.
        :param user_pool: (experimental) User provided Cognito UserPool. Default: - a userpool will be created.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66f23d93fd801ead273f3929575f98db1f55b731d28dcb3ec2b15e575581d50e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = UserIdentityProps(
            identity_pool_options=identity_pool_options, user_pool=user_pool
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="identityPool")
    def identity_pool(
        self,
    ) -> _aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPool:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPool, jsii.get(self, "identityPool"))

    @builtins.property
    @jsii.member(jsii_name="userPool")
    def user_pool(self) -> _aws_cdk_aws_cognito_ceddda9d.UserPool:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_cognito_ceddda9d.UserPool, jsii.get(self, "userPool"))

    @builtins.property
    @jsii.member(jsii_name="userPoolClient")
    def user_pool_client(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPoolClient]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPoolClient], jsii.get(self, "userPoolClient"))


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/identity.UserIdentityProps",
    jsii_struct_bases=[],
    name_mapping={
        "identity_pool_options": "identityPoolOptions",
        "user_pool": "userPool",
    },
)
class UserIdentityProps:
    def __init__(
        self,
        *,
        identity_pool_options: typing.Optional[typing.Union[_aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPoolProps, typing.Dict[builtins.str, typing.Any]]] = None,
        user_pool: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool] = None,
    ) -> None:
        '''(experimental) Properties which configures the Identity Pool.

        :param identity_pool_options: (experimental) Configuration for the Identity Pool.
        :param user_pool: (experimental) User provided Cognito UserPool. Default: - a userpool will be created.

        :stability: experimental
        '''
        if isinstance(identity_pool_options, dict):
            identity_pool_options = _aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPoolProps(**identity_pool_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c256d340ffec1f29962d3f56281b950c3768952c6bae18e26952d21477b01ce)
            check_type(argname="argument identity_pool_options", value=identity_pool_options, expected_type=type_hints["identity_pool_options"])
            check_type(argname="argument user_pool", value=user_pool, expected_type=type_hints["user_pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identity_pool_options is not None:
            self._values["identity_pool_options"] = identity_pool_options
        if user_pool is not None:
            self._values["user_pool"] = user_pool

    @builtins.property
    def identity_pool_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPoolProps]:
        '''(experimental) Configuration for the Identity Pool.

        :stability: experimental
        '''
        result = self._values.get("identity_pool_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPoolProps], result)

    @builtins.property
    def user_pool(self) -> typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool]:
        '''(experimental) User provided Cognito UserPool.

        :default: - a userpool will be created.

        :stability: experimental
        '''
        result = self._values.get("user_pool")
        return typing.cast(typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserIdentityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "UserIdentity",
    "UserIdentityProps",
]

publication.publish()

def _typecheckingstub__66f23d93fd801ead273f3929575f98db1f55b731d28dcb3ec2b15e575581d50e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    identity_pool_options: typing.Optional[typing.Union[_aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPoolProps, typing.Dict[builtins.str, typing.Any]]] = None,
    user_pool: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c256d340ffec1f29962d3f56281b950c3768952c6bae18e26952d21477b01ce(
    *,
    identity_pool_options: typing.Optional[typing.Union[_aws_cdk_aws_cognito_identitypool_alpha_e0ee7798.IdentityPoolProps, typing.Dict[builtins.str, typing.Any]]] = None,
    user_pool: typing.Optional[_aws_cdk_aws_cognito_ceddda9d.UserPool] = None,
) -> None:
    """Type checking stubs"""
    pass
