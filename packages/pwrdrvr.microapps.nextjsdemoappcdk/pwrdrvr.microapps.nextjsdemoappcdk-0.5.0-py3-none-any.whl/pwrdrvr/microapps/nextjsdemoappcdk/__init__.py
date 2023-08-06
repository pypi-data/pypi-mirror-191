'''
![Build/Deploy CI](https://github.com/pwrdrvr/microapps-app-nextjs-demo/actions/workflows/ci.yml/badge.svg) ![JSII](https://github.com/pwrdrvr/microapps-app-nextjs-demo/actions/workflows/jsii.yml/badge.svg) ![Release](https://github.com/pwrdrvr/microapps-app-nextjs-demo/actions/workflows/release.yml/badge.svg)

# Overview

This is the Release Console for the MicroApps framework.

# Development

* `nvm use`
* For Mac

  * Install Xcode
  * `xcode-select --install`
  * `brew install vips`
* `npm i`
* `npm run dev`
* Open in browser: `http://localhost:3000/nextjs-demo`

# Publish New Version of Microapp

See GitHub Actions workflows for example commands.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk
import aws_cdk.aws_lambda
import constructs


@jsii.interface(
    jsii_type="@pwrdrvr/microapps-app-nextjs-demo-cdk.IMicroAppsAppNextjsDemo"
)
class IMicroAppsAppNextjsDemo(typing_extensions.Protocol):
    '''Represents an app.'''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.IFunction:
        '''The Lambda function created.'''
        ...


class _IMicroAppsAppNextjsDemoProxy:
    '''Represents an app.'''

    __jsii_type__: typing.ClassVar[str] = "@pwrdrvr/microapps-app-nextjs-demo-cdk.IMicroAppsAppNextjsDemo"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.IFunction:
        '''The Lambda function created.'''
        return typing.cast(aws_cdk.aws_lambda.IFunction, jsii.get(self, "lambdaFunction"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMicroAppsAppNextjsDemo).__jsii_proxy_class__ = lambda : _IMicroAppsAppNextjsDemoProxy


@jsii.implements(IMicroAppsAppNextjsDemo)
class MicroAppsAppNextjsDemo(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@pwrdrvr/microapps-app-nextjs-demo-cdk.MicroAppsAppNextjsDemo",
):
    '''MicroApps Next.js demo app.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        function_name: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
    ) -> None:
        '''Lambda function, permissions, and assets used by the app.

        :param scope: -
        :param id: -
        :param function_name: Name for the Lambda function. While this can be random, it's much easier to make it deterministic so it can be computed for passing to ``microapps-publish``. Default: auto-generated
        :param node_env: NODE_ENV to set on Lambda.
        :param removal_policy: Removal Policy to pass to assets (e.g. Lambda function).
        '''
        props = MicroAppsAppNextjsDemoProps(
            function_name=function_name,
            node_env=node_env,
            removal_policy=removal_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.IFunction:
        '''The Lambda function created.'''
        return typing.cast(aws_cdk.aws_lambda.IFunction, jsii.get(self, "lambdaFunction"))


@jsii.data_type(
    jsii_type="@pwrdrvr/microapps-app-nextjs-demo-cdk.MicroAppsAppNextjsDemoProps",
    jsii_struct_bases=[],
    name_mapping={
        "function_name": "functionName",
        "node_env": "nodeEnv",
        "removal_policy": "removalPolicy",
    },
)
class MicroAppsAppNextjsDemoProps:
    def __init__(
        self,
        *,
        function_name: typing.Optional[builtins.str] = None,
        node_env: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
    ) -> None:
        '''Properties to initialize an instance of ``MicroAppsAppNextjsDemo``.

        :param function_name: Name for the Lambda function. While this can be random, it's much easier to make it deterministic so it can be computed for passing to ``microapps-publish``. Default: auto-generated
        :param node_env: NODE_ENV to set on Lambda.
        :param removal_policy: Removal Policy to pass to assets (e.g. Lambda function).
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if function_name is not None:
            self._values["function_name"] = function_name
        if node_env is not None:
            self._values["node_env"] = node_env
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''Name for the Lambda function.

        While this can be random, it's much easier to make it deterministic
        so it can be computed for passing to ``microapps-publish``.

        :default: auto-generated
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_env(self) -> typing.Optional[builtins.str]:
        '''NODE_ENV to set on Lambda.'''
        result = self._values.get("node_env")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.RemovalPolicy]:
        '''Removal Policy to pass to assets (e.g. Lambda function).'''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[aws_cdk.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MicroAppsAppNextjsDemoProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IMicroAppsAppNextjsDemo",
    "MicroAppsAppNextjsDemo",
    "MicroAppsAppNextjsDemoProps",
]

publication.publish()
