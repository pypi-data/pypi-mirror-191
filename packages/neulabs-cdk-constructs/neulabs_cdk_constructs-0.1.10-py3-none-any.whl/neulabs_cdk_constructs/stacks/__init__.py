import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kinesisfirehose as _aws_cdk_aws_kinesisfirehose_ceddda9d
import aws_cdk.aws_resourcegroups as _aws_cdk_aws_resourcegroups_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8
from ..common import BaseTagProps as _BaseTagProps_fd4c4d78


class BaseStack(
    _aws_cdk_ceddda9d.Stack,
    metaclass=jsii.JSIIMeta,
    jsii_type="neulabs-cdk-constructs.stacks.BaseStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        stage: builtins.str,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param stage: 
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8c3906f799f67d5a7e24ee1c0e82ba15bc0ee085154161fd98d129777139786)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BaseStackProps(
            stage=stage,
            analytics_reporting=analytics_reporting,
            cross_region_references=cross_region_references,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addBaseTags")
    def add_base_tags(
        self,
        model: typing.Any,
        *,
        business_unit: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        repository_name: typing.Optional[builtins.str] = None,
        repository_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param model: -
        :param business_unit: 
        :param domain: 
        :param repository_name: 
        :param repository_version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e0c1253c5ad66fddcf1f03ca1661e0dcff75fd4de68d28896990299d9ee25bc)
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
        props = _BaseTagProps_fd4c4d78(
            business_unit=business_unit,
            domain=domain,
            repository_name=repository_name,
            repository_version=repository_version,
        )

        return typing.cast(None, jsii.invoke(self, "addBaseTags", [model, props]))

    @jsii.member(jsii_name="createResourcesGroup")
    def create_resources_group(self) -> _aws_cdk_aws_resourcegroups_ceddda9d.CfnGroup:
        return typing.cast(_aws_cdk_aws_resourcegroups_ceddda9d.CfnGroup, jsii.invoke(self, "createResourcesGroup", []))

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stage"))

    @stage.setter
    def stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b9151b72dacaa74fd06951252aec9571e464b1e9decde23f52a407d018d0ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stage", value)


@jsii.data_type(
    jsii_type="neulabs-cdk-constructs.stacks.BaseStackProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.StackProps],
    name_mapping={
        "analytics_reporting": "analyticsReporting",
        "cross_region_references": "crossRegionReferences",
        "description": "description",
        "env": "env",
        "stack_name": "stackName",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
        "stage": "stage",
    },
)
class BaseStackProps(_aws_cdk_ceddda9d.StackProps):
    def __init__(
        self,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
        stage: builtins.str,
    ) -> None:
        '''
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        :param stage: 
        '''
        if isinstance(env, dict):
            env = _aws_cdk_ceddda9d.Environment(**env)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31847f9f18c83f9e0519164c5b05a3736c0afdc5714045805f62f54bf0f2a675)
            check_type(argname="argument analytics_reporting", value=analytics_reporting, expected_type=type_hints["analytics_reporting"])
            check_type(argname="argument cross_region_references", value=cross_region_references, expected_type=type_hints["cross_region_references"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument synthesizer", value=synthesizer, expected_type=type_hints["synthesizer"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection", value=termination_protection, expected_type=type_hints["termination_protection"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stage": stage,
        }
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if cross_region_references is not None:
            self._values["cross_region_references"] = cross_region_references
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if synthesizer is not None:
            self._values["synthesizer"] = synthesizer
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in this Stack.

        :default:

        ``analyticsReporting`` setting of containing ``App``, or value of
        'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cross_region_references(self) -> typing.Optional[builtins.bool]:
        '''Enable this flag to allow native cross region stack references.

        Enabling this will create a CloudFormation custom resource
        in both the producing stack and consuming stack in order to perform the export/import

        This feature is currently experimental

        :default: false
        '''
        result = self._values.get("cross_region_references")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[_aws_cdk_ceddda9d.Environment]:
        '''The AWS environment (account/region) where this stack will be deployed.

        Set the ``region``/``account`` fields of ``env`` to either a concrete value to
        select the indicated environment (recommended for production stacks), or to
        the values of environment variables
        ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment
        depend on the AWS credentials/configuration that the CDK CLI is executed
        under (recommended for development stacks).

        If the ``Stack`` is instantiated inside a ``Stage``, any undefined
        ``region``/``account`` fields from ``env`` will default to the same field on the
        encompassing ``Stage``, if configured there.

        If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the
        Stack will be considered "*environment-agnostic*"". Environment-agnostic
        stacks can be deployed to any environment but may not be able to take
        advantage of all features of the CDK. For example, they will not be able to
        use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not
        automatically translate Service Principals to the right format based on the
        environment's AWS partition, and other such enhancements.

        :default:

        - The environment of the containing ``Stage`` if available,
        otherwise create the stack will be environment-agnostic.

        Example::

            // Use a concrete account and region to deploy this stack to:
            // `.account` and `.region` will simply return these values.
            new Stack(app, 'Stack1', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              },
            });
            
            // Use the CLI's current credentials to determine the target environment:
            // `.account` and `.region` will reflect the account+region the CLI
            // is configured to use (based on the user CLI credentials)
            new Stack(app, 'Stack2', {
              env: {
                account: process.env.CDK_DEFAULT_ACCOUNT,
                region: process.env.CDK_DEFAULT_REGION
              },
            });
            
            // Define multiple stacks stage associated with an environment
            const myStage = new Stage(app, 'MyStage', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              }
            });
            
            // both of these stacks will use the stage's account/region:
            // `.account` and `.region` will resolve to the concrete values as above
            new MyStack(myStage, 'Stack1');
            new YourStack(myStage, 'Stack2');
            
            // Define an environment-agnostic stack:
            // `.account` and `.region` will resolve to `{ "Ref": "AWS::AccountId" }` and `{ "Ref": "AWS::Region" }` respectively.
            // which will only resolve to actual values by CloudFormation during deployment.
            new MyStack(app, 'Stack1');
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Environment], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Name to deploy the stack with.

        :default: - Derived from construct path.
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synthesizer(self) -> typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer]:
        '''Synthesis method to use while deploying this stack.

        :default:

        - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag
        is set, ``LegacyStackSynthesizer`` otherwise.
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Stack tags that will be applied to all the taggable resources and the stack itself.

        :default: {}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable termination protection for this stack.

        :default: false
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stage(self) -> builtins.str:
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="neulabs-cdk-constructs.stacks.EndpointType")
class EndpointType(enum.Enum):
    METRICS = "METRICS"
    LOGS = "LOGS"


@jsii.enum(jsii_type="neulabs-cdk-constructs.stacks.EndpointUrlLogs")
class EndpointUrlLogs(enum.Enum):
    EU_LOGS = "EU_LOGS"
    US_LOGS = "US_LOGS"


@jsii.enum(jsii_type="neulabs-cdk-constructs.stacks.EndpointUrlMetrics")
class EndpointUrlMetrics(enum.Enum):
    EU_METRICS = "EU_METRICS"
    US_METRICS = "US_METRICS"


class GithubOIDCStack(
    BaseStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="neulabs-cdk-constructs.stacks.GithubOIDCStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        github_repository: builtins.str,
        github_user: builtins.str,
        token_action: "TokenActions",
        cdk_deploy_role_managed_policies: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy]] = None,
        cdk_deploy_role_policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        token_action_custom: typing.Optional[builtins.str] = None,
        stage: builtins.str,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param github_repository: 
        :param github_user: 
        :param token_action: 
        :param cdk_deploy_role_managed_policies: 
        :param cdk_deploy_role_policy_statements: 
        :param token_action_custom: 
        :param stage: 
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2edd5d0fbd3812c3fe9c4b32c89e2358255a628a9b08ba813843df326922709d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GithubOIDCStackStackProps(
            github_repository=github_repository,
            github_user=github_user,
            token_action=token_action,
            cdk_deploy_role_managed_policies=cdk_deploy_role_managed_policies,
            cdk_deploy_role_policy_statements=cdk_deploy_role_policy_statements,
            token_action_custom=token_action_custom,
            stage=stage,
            analytics_reporting=analytics_reporting,
            cross_region_references=cross_region_references,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createCdkBootstrapRole")
    def create_cdk_bootstrap_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.invoke(self, "createCdkBootstrapRole", []))

    @jsii.member(jsii_name="createCdkDeployRole")
    def create_cdk_deploy_role(
        self,
        managed_policies: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy]] = None,
        policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    ) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''
        :param managed_policies: -
        :param policy_statements: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75edbe2b52327f605fc5a2ff70cc1370a8eacbbdb13d1db237f3dd4b9ee5c36a)
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
            check_type(argname="argument policy_statements", value=policy_statements, expected_type=type_hints["policy_statements"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.invoke(self, "createCdkDeployRole", [managed_policies, policy_statements]))

    @jsii.member(jsii_name="createOidcRole")
    def create_oidc_role(
        self,
        provider_url: builtins.str,
        token: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''
        :param provider_url: -
        :param token: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b14133f278789eb8e1e684f0c9a72082f2f8df9af6f48929c84547c5b70133f)
            check_type(argname="argument provider_url", value=provider_url, expected_type=type_hints["provider_url"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.invoke(self, "createOidcRole", [provider_url, token]))

    @jsii.member(jsii_name="createTokenAction")
    def create_token_action(
        self,
        token_action: "TokenActions",
        github_user: builtins.str,
        github_repository: builtins.str,
        token_action_custom: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''
        :param token_action: -
        :param github_user: -
        :param github_repository: -
        :param token_action_custom: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df3994aae471bf2921d73f61b727d533a660da9028b31a684c1d20a82a6cbef)
            check_type(argname="argument token_action", value=token_action, expected_type=type_hints["token_action"])
            check_type(argname="argument github_user", value=github_user, expected_type=type_hints["github_user"])
            check_type(argname="argument github_repository", value=github_repository, expected_type=type_hints["github_repository"])
            check_type(argname="argument token_action_custom", value=token_action_custom, expected_type=type_hints["token_action_custom"])
        return typing.cast(builtins.str, jsii.invoke(self, "createTokenAction", [token_action, github_user, github_repository, token_action_custom]))

    @builtins.property
    @jsii.member(jsii_name="cdkBootstrapRole")
    def cdk_bootstrap_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "cdkBootstrapRole"))

    @cdk_bootstrap_role.setter
    def cdk_bootstrap_role(self, value: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c045fafb37ff9100ec2a91b556074f24b5beceb07ea909463febe37129404d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdkBootstrapRole", value)

    @builtins.property
    @jsii.member(jsii_name="cdkDeployRole")
    def cdk_deploy_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "cdkDeployRole"))

    @cdk_deploy_role.setter
    def cdk_deploy_role(self, value: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7160e09388553b939314d9077e28ede6aab4965b51fca156dbced70bb51e1360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdkDeployRole", value)

    @builtins.property
    @jsii.member(jsii_name="githubRepository")
    def github_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "githubRepository"))

    @github_repository.setter
    def github_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87080802d68a6c0233ed49d6447901302ad8092daefae8287833b0fe17dfc683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "githubRepository", value)

    @builtins.property
    @jsii.member(jsii_name="githubUser")
    def github_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "githubUser"))

    @github_user.setter
    def github_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6642170ad325f27b7571dc1aaf9495313cdaa57532ee00e4c7c915196f8abb5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "githubUser", value)

    @builtins.property
    @jsii.member(jsii_name="oidcRole")
    def oidc_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "oidcRole"))

    @oidc_role.setter
    def oidc_role(self, value: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d4fbc01c038ea99e7305875f913ef979d93b13e57088b320555b4b1d5208e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oidcRole", value)

    @builtins.property
    @jsii.member(jsii_name="tokenAction")
    def token_action(self) -> "TokenActions":
        return typing.cast("TokenActions", jsii.get(self, "tokenAction"))

    @token_action.setter
    def token_action(self, value: "TokenActions") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03895cafb560af8d2a45fcda637206e2b68b92ede5263fa3e0238974b403e4fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenAction", value)

    @builtins.property
    @jsii.member(jsii_name="cdkDeployRoleManagedPolicies")
    def cdk_deploy_role_managed_policies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy]]:
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy]], jsii.get(self, "cdkDeployRoleManagedPolicies"))

    @cdk_deploy_role_managed_policies.setter
    def cdk_deploy_role_managed_policies(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4633d11a7f22626b7ed31e856302b0236ff8c5086b41ce88ecd332d21b20809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdkDeployRoleManagedPolicies", value)

    @builtins.property
    @jsii.member(jsii_name="cdkDeployRolePolicyStatements")
    def cdk_deploy_role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]]:
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]], jsii.get(self, "cdkDeployRolePolicyStatements"))

    @cdk_deploy_role_policy_statements.setter
    def cdk_deploy_role_policy_statements(
        self,
        value: typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__802ab8bfa128a99b9f73f4fb84580a1332025cf010c6902f197ca120289e2d4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdkDeployRolePolicyStatements", value)


@jsii.data_type(
    jsii_type="neulabs-cdk-constructs.stacks.GithubOIDCStackStackProps",
    jsii_struct_bases=[BaseStackProps],
    name_mapping={
        "analytics_reporting": "analyticsReporting",
        "cross_region_references": "crossRegionReferences",
        "description": "description",
        "env": "env",
        "stack_name": "stackName",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
        "stage": "stage",
        "github_repository": "githubRepository",
        "github_user": "githubUser",
        "token_action": "tokenAction",
        "cdk_deploy_role_managed_policies": "cdkDeployRoleManagedPolicies",
        "cdk_deploy_role_policy_statements": "cdkDeployRolePolicyStatements",
        "token_action_custom": "tokenActionCustom",
    },
)
class GithubOIDCStackStackProps(BaseStackProps):
    def __init__(
        self,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
        stage: builtins.str,
        github_repository: builtins.str,
        github_user: builtins.str,
        token_action: "TokenActions",
        cdk_deploy_role_managed_policies: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy]] = None,
        cdk_deploy_role_policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        token_action_custom: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        :param stage: 
        :param github_repository: 
        :param github_user: 
        :param token_action: 
        :param cdk_deploy_role_managed_policies: 
        :param cdk_deploy_role_policy_statements: 
        :param token_action_custom: 
        '''
        if isinstance(env, dict):
            env = _aws_cdk_ceddda9d.Environment(**env)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a443823344e7cbe6b0fd244775db3c260d3fff85df631e748d2ff85ad31f1fe)
            check_type(argname="argument analytics_reporting", value=analytics_reporting, expected_type=type_hints["analytics_reporting"])
            check_type(argname="argument cross_region_references", value=cross_region_references, expected_type=type_hints["cross_region_references"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument synthesizer", value=synthesizer, expected_type=type_hints["synthesizer"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection", value=termination_protection, expected_type=type_hints["termination_protection"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument github_repository", value=github_repository, expected_type=type_hints["github_repository"])
            check_type(argname="argument github_user", value=github_user, expected_type=type_hints["github_user"])
            check_type(argname="argument token_action", value=token_action, expected_type=type_hints["token_action"])
            check_type(argname="argument cdk_deploy_role_managed_policies", value=cdk_deploy_role_managed_policies, expected_type=type_hints["cdk_deploy_role_managed_policies"])
            check_type(argname="argument cdk_deploy_role_policy_statements", value=cdk_deploy_role_policy_statements, expected_type=type_hints["cdk_deploy_role_policy_statements"])
            check_type(argname="argument token_action_custom", value=token_action_custom, expected_type=type_hints["token_action_custom"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stage": stage,
            "github_repository": github_repository,
            "github_user": github_user,
            "token_action": token_action,
        }
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if cross_region_references is not None:
            self._values["cross_region_references"] = cross_region_references
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if synthesizer is not None:
            self._values["synthesizer"] = synthesizer
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection
        if cdk_deploy_role_managed_policies is not None:
            self._values["cdk_deploy_role_managed_policies"] = cdk_deploy_role_managed_policies
        if cdk_deploy_role_policy_statements is not None:
            self._values["cdk_deploy_role_policy_statements"] = cdk_deploy_role_policy_statements
        if token_action_custom is not None:
            self._values["token_action_custom"] = token_action_custom

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in this Stack.

        :default:

        ``analyticsReporting`` setting of containing ``App``, or value of
        'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cross_region_references(self) -> typing.Optional[builtins.bool]:
        '''Enable this flag to allow native cross region stack references.

        Enabling this will create a CloudFormation custom resource
        in both the producing stack and consuming stack in order to perform the export/import

        This feature is currently experimental

        :default: false
        '''
        result = self._values.get("cross_region_references")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[_aws_cdk_ceddda9d.Environment]:
        '''The AWS environment (account/region) where this stack will be deployed.

        Set the ``region``/``account`` fields of ``env`` to either a concrete value to
        select the indicated environment (recommended for production stacks), or to
        the values of environment variables
        ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment
        depend on the AWS credentials/configuration that the CDK CLI is executed
        under (recommended for development stacks).

        If the ``Stack`` is instantiated inside a ``Stage``, any undefined
        ``region``/``account`` fields from ``env`` will default to the same field on the
        encompassing ``Stage``, if configured there.

        If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the
        Stack will be considered "*environment-agnostic*"". Environment-agnostic
        stacks can be deployed to any environment but may not be able to take
        advantage of all features of the CDK. For example, they will not be able to
        use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not
        automatically translate Service Principals to the right format based on the
        environment's AWS partition, and other such enhancements.

        :default:

        - The environment of the containing ``Stage`` if available,
        otherwise create the stack will be environment-agnostic.

        Example::

            // Use a concrete account and region to deploy this stack to:
            // `.account` and `.region` will simply return these values.
            new Stack(app, 'Stack1', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              },
            });
            
            // Use the CLI's current credentials to determine the target environment:
            // `.account` and `.region` will reflect the account+region the CLI
            // is configured to use (based on the user CLI credentials)
            new Stack(app, 'Stack2', {
              env: {
                account: process.env.CDK_DEFAULT_ACCOUNT,
                region: process.env.CDK_DEFAULT_REGION
              },
            });
            
            // Define multiple stacks stage associated with an environment
            const myStage = new Stage(app, 'MyStage', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              }
            });
            
            // both of these stacks will use the stage's account/region:
            // `.account` and `.region` will resolve to the concrete values as above
            new MyStack(myStage, 'Stack1');
            new YourStack(myStage, 'Stack2');
            
            // Define an environment-agnostic stack:
            // `.account` and `.region` will resolve to `{ "Ref": "AWS::AccountId" }` and `{ "Ref": "AWS::Region" }` respectively.
            // which will only resolve to actual values by CloudFormation during deployment.
            new MyStack(app, 'Stack1');
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Environment], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Name to deploy the stack with.

        :default: - Derived from construct path.
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synthesizer(self) -> typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer]:
        '''Synthesis method to use while deploying this stack.

        :default:

        - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag
        is set, ``LegacyStackSynthesizer`` otherwise.
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Stack tags that will be applied to all the taggable resources and the stack itself.

        :default: {}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable termination protection for this stack.

        :default: false
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stage(self) -> builtins.str:
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def github_repository(self) -> builtins.str:
        result = self._values.get("github_repository")
        assert result is not None, "Required property 'github_repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def github_user(self) -> builtins.str:
        result = self._values.get("github_user")
        assert result is not None, "Required property 'github_user' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_action(self) -> "TokenActions":
        result = self._values.get("token_action")
        assert result is not None, "Required property 'token_action' is missing"
        return typing.cast("TokenActions", result)

    @builtins.property
    def cdk_deploy_role_managed_policies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy]]:
        result = self._values.get("cdk_deploy_role_managed_policies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy]], result)

    @builtins.property
    def cdk_deploy_role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]]:
        result = self._values.get("cdk_deploy_role_policy_statements")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]], result)

    @builtins.property
    def token_action_custom(self) -> typing.Optional[builtins.str]:
        result = self._values.get("token_action_custom")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubOIDCStackStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NewRelicStack(
    BaseStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="neulabs-cdk-constructs.stacks.NewRelicStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        new_relic_account_id: builtins.str,
        new_relic_api_url_logs: EndpointUrlLogs,
        new_relic_api_url_metrics: EndpointUrlMetrics,
        new_relic_bucket_name: builtins.str,
        new_relic_license_key: builtins.str,
        stage: builtins.str,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param new_relic_account_id: 
        :param new_relic_api_url_logs: 
        :param new_relic_api_url_metrics: 
        :param new_relic_bucket_name: 
        :param new_relic_license_key: 
        :param stage: 
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66070d9b3140cc0a446c1ad3578a567763e44b80c35f76d1f1ad96cc4b946fb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NewRelicStackProps(
            new_relic_account_id=new_relic_account_id,
            new_relic_api_url_logs=new_relic_api_url_logs,
            new_relic_api_url_metrics=new_relic_api_url_metrics,
            new_relic_bucket_name=new_relic_bucket_name,
            new_relic_license_key=new_relic_license_key,
            stage=stage,
            analytics_reporting=analytics_reporting,
            cross_region_references=cross_region_references,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createCloudwatchLogsStreamRole")
    def create_cloudwatch_logs_stream_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.invoke(self, "createCloudwatchLogsStreamRole", []))

    @jsii.member(jsii_name="createCloudwatchMetricStream")
    def create_cloudwatch_metric_stream(
        self,
        role_arn: builtins.str,
        firehose_arn: builtins.str,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream:
        '''
        :param role_arn: -
        :param firehose_arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99bce3b29be5c04fd361caab5cf05193a203e18b51f8401c627d9d1cbe985739)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument firehose_arn", value=firehose_arn, expected_type=type_hints["firehose_arn"])
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream, jsii.invoke(self, "createCloudwatchMetricStream", [role_arn, firehose_arn]))

    @jsii.member(jsii_name="createFirehoseBucket")
    def create_firehose_bucket(
        self,
        new_relic_bucket_name: builtins.str,
    ) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''
        :param new_relic_bucket_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0af065866a83d51eb0e0efade26989482a578f474975fbb0c354e6b35101cd54)
            check_type(argname="argument new_relic_bucket_name", value=new_relic_bucket_name, expected_type=type_hints["new_relic_bucket_name"])
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.invoke(self, "createFirehoseBucket", [new_relic_bucket_name]))

    @jsii.member(jsii_name="createFirehoseRole")
    def create_firehose_role(
        self,
        new_relic_firehose_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    ) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''
        :param new_relic_firehose_bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7a7fa119bd27321fd2c372ff88c0e31f6399a8005d53db8ae1893206db7c83)
            check_type(argname="argument new_relic_firehose_bucket", value=new_relic_firehose_bucket, expected_type=type_hints["new_relic_firehose_bucket"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.invoke(self, "createFirehoseRole", [new_relic_firehose_bucket]))

    @jsii.member(jsii_name="createFirehoseStream")
    def create_firehose_stream(
        self,
        new_relic_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
        endpoint_type: EndpointType,
        endpoint_url: builtins.str,
        new_relic_license_ley: builtins.str,
    ) -> _aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream:
        '''
        :param new_relic_bucket: -
        :param role: -
        :param endpoint_type: -
        :param endpoint_url: -
        :param new_relic_license_ley: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba82381b3ec49fd57c738767405e96e64c27f63c6f7bcfd505efe3e141fa1274)
            check_type(argname="argument new_relic_bucket", value=new_relic_bucket, expected_type=type_hints["new_relic_bucket"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument endpoint_url", value=endpoint_url, expected_type=type_hints["endpoint_url"])
            check_type(argname="argument new_relic_license_ley", value=new_relic_license_ley, expected_type=type_hints["new_relic_license_ley"])
        return typing.cast(_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream, jsii.invoke(self, "createFirehoseStream", [new_relic_bucket, role, endpoint_type, endpoint_url, new_relic_license_ley]))

    @jsii.member(jsii_name="createNewRelicRole")
    def create_new_relic_role(
        self,
        new_relic_account_id: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''
        :param new_relic_account_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7305bbdc447fe35fa9f514bed3ae462d85bc16a0c458091c09de9a4e282c8539)
            check_type(argname="argument new_relic_account_id", value=new_relic_account_id, expected_type=type_hints["new_relic_account_id"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.invoke(self, "createNewRelicRole", [new_relic_account_id]))

    @jsii.member(jsii_name="createSecrets")
    def create_secrets(
        self,
        new_relic_account_id: builtins.str,
        new_relic_license_ley: builtins.str,
    ) -> _aws_cdk_aws_secretsmanager_ceddda9d.Secret:
        '''
        :param new_relic_account_id: -
        :param new_relic_license_ley: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84c8a462bfc935cd2f4168debc558f4856a86d613033850469d399df40ccaaf)
            check_type(argname="argument new_relic_account_id", value=new_relic_account_id, expected_type=type_hints["new_relic_account_id"])
            check_type(argname="argument new_relic_license_ley", value=new_relic_license_ley, expected_type=type_hints["new_relic_license_ley"])
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.Secret, jsii.invoke(self, "createSecrets", [new_relic_account_id, new_relic_license_ley]))

    @builtins.property
    @jsii.member(jsii_name="newRelicBucket")
    def new_relic_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "newRelicBucket"))

    @new_relic_bucket.setter
    def new_relic_bucket(self, value: _aws_cdk_aws_s3_ceddda9d.IBucket) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1acc91a446ee8b01943fd9805797d3ddeb6078e2b5c31fb8ac4b789382176ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newRelicBucket", value)

    @builtins.property
    @jsii.member(jsii_name="newRelicFirehoseRole")
    def new_relic_firehose_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "newRelicFirehoseRole"))

    @new_relic_firehose_role.setter
    def new_relic_firehose_role(self, value: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55ce2c39bb4a1970fceba0aeae62534edc819f3a962bc673fb639fa05ff48ff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newRelicFirehoseRole", value)

    @builtins.property
    @jsii.member(jsii_name="newRelicIntegrationRole")
    def new_relic_integration_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "newRelicIntegrationRole"))

    @new_relic_integration_role.setter
    def new_relic_integration_role(
        self,
        value: _aws_cdk_aws_iam_ceddda9d.IRole,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8f4d498840b27542b7c21375598d3597d18f2825933afdd40cfff7f49f54ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newRelicIntegrationRole", value)

    @builtins.property
    @jsii.member(jsii_name="newRelicSecret")
    def new_relic_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "newRelicSecret"))

    @new_relic_secret.setter
    def new_relic_secret(
        self,
        value: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ac8027091ea0e5a24b81302fdbf87847ed9ce182ee77c4e174286d7ce492c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newRelicSecret", value)

    @builtins.property
    @jsii.member(jsii_name="newRelicCloudwatchLogsStreamRole")
    def new_relic_cloudwatch_logs_stream_role(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "newRelicCloudwatchLogsStreamRole"))

    @new_relic_cloudwatch_logs_stream_role.setter
    def new_relic_cloudwatch_logs_stream_role(
        self,
        value: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9f75ef9eeacb91adae0e7c7a6a31805c523154e7854c5df972941469f6b723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newRelicCloudwatchLogsStreamRole", value)

    @builtins.property
    @jsii.member(jsii_name="newRelicFirehoseLogs")
    def new_relic_firehose_logs(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream]:
        return typing.cast(typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream], jsii.get(self, "newRelicFirehoseLogs"))

    @new_relic_firehose_logs.setter
    def new_relic_firehose_logs(
        self,
        value: typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e9574b6c7d2bbbd95c0e93a31f3c1e665125256e90c5c4fe8ceacd450d74a85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newRelicFirehoseLogs", value)

    @builtins.property
    @jsii.member(jsii_name="newRelicFirehoseMetrics")
    def new_relic_firehose_metrics(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream]:
        return typing.cast(typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream], jsii.get(self, "newRelicFirehoseMetrics"))

    @new_relic_firehose_metrics.setter
    def new_relic_firehose_metrics(
        self,
        value: typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb544dfdd2d81e3c5390d607beb842fecf8d5b037e4b42e634c845726be00d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newRelicFirehoseMetrics", value)


@jsii.data_type(
    jsii_type="neulabs-cdk-constructs.stacks.NewRelicStackProps",
    jsii_struct_bases=[BaseStackProps],
    name_mapping={
        "analytics_reporting": "analyticsReporting",
        "cross_region_references": "crossRegionReferences",
        "description": "description",
        "env": "env",
        "stack_name": "stackName",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
        "stage": "stage",
        "new_relic_account_id": "newRelicAccountId",
        "new_relic_api_url_logs": "newRelicApiUrlLogs",
        "new_relic_api_url_metrics": "newRelicApiUrlMetrics",
        "new_relic_bucket_name": "newRelicBucketName",
        "new_relic_license_key": "newRelicLicenseKey",
    },
)
class NewRelicStackProps(BaseStackProps):
    def __init__(
        self,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
        stage: builtins.str,
        new_relic_account_id: builtins.str,
        new_relic_api_url_logs: EndpointUrlLogs,
        new_relic_api_url_metrics: EndpointUrlMetrics,
        new_relic_bucket_name: builtins.str,
        new_relic_license_key: builtins.str,
    ) -> None:
        '''
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        :param stage: 
        :param new_relic_account_id: 
        :param new_relic_api_url_logs: 
        :param new_relic_api_url_metrics: 
        :param new_relic_bucket_name: 
        :param new_relic_license_key: 
        '''
        if isinstance(env, dict):
            env = _aws_cdk_ceddda9d.Environment(**env)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b7c9c4c2b943358cff93dc3eaf101b1711879fa1e3fc653e137feb6a4c418c)
            check_type(argname="argument analytics_reporting", value=analytics_reporting, expected_type=type_hints["analytics_reporting"])
            check_type(argname="argument cross_region_references", value=cross_region_references, expected_type=type_hints["cross_region_references"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument synthesizer", value=synthesizer, expected_type=type_hints["synthesizer"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection", value=termination_protection, expected_type=type_hints["termination_protection"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument new_relic_account_id", value=new_relic_account_id, expected_type=type_hints["new_relic_account_id"])
            check_type(argname="argument new_relic_api_url_logs", value=new_relic_api_url_logs, expected_type=type_hints["new_relic_api_url_logs"])
            check_type(argname="argument new_relic_api_url_metrics", value=new_relic_api_url_metrics, expected_type=type_hints["new_relic_api_url_metrics"])
            check_type(argname="argument new_relic_bucket_name", value=new_relic_bucket_name, expected_type=type_hints["new_relic_bucket_name"])
            check_type(argname="argument new_relic_license_key", value=new_relic_license_key, expected_type=type_hints["new_relic_license_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stage": stage,
            "new_relic_account_id": new_relic_account_id,
            "new_relic_api_url_logs": new_relic_api_url_logs,
            "new_relic_api_url_metrics": new_relic_api_url_metrics,
            "new_relic_bucket_name": new_relic_bucket_name,
            "new_relic_license_key": new_relic_license_key,
        }
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if cross_region_references is not None:
            self._values["cross_region_references"] = cross_region_references
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if synthesizer is not None:
            self._values["synthesizer"] = synthesizer
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in this Stack.

        :default:

        ``analyticsReporting`` setting of containing ``App``, or value of
        'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cross_region_references(self) -> typing.Optional[builtins.bool]:
        '''Enable this flag to allow native cross region stack references.

        Enabling this will create a CloudFormation custom resource
        in both the producing stack and consuming stack in order to perform the export/import

        This feature is currently experimental

        :default: false
        '''
        result = self._values.get("cross_region_references")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[_aws_cdk_ceddda9d.Environment]:
        '''The AWS environment (account/region) where this stack will be deployed.

        Set the ``region``/``account`` fields of ``env`` to either a concrete value to
        select the indicated environment (recommended for production stacks), or to
        the values of environment variables
        ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment
        depend on the AWS credentials/configuration that the CDK CLI is executed
        under (recommended for development stacks).

        If the ``Stack`` is instantiated inside a ``Stage``, any undefined
        ``region``/``account`` fields from ``env`` will default to the same field on the
        encompassing ``Stage``, if configured there.

        If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the
        Stack will be considered "*environment-agnostic*"". Environment-agnostic
        stacks can be deployed to any environment but may not be able to take
        advantage of all features of the CDK. For example, they will not be able to
        use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not
        automatically translate Service Principals to the right format based on the
        environment's AWS partition, and other such enhancements.

        :default:

        - The environment of the containing ``Stage`` if available,
        otherwise create the stack will be environment-agnostic.

        Example::

            // Use a concrete account and region to deploy this stack to:
            // `.account` and `.region` will simply return these values.
            new Stack(app, 'Stack1', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              },
            });
            
            // Use the CLI's current credentials to determine the target environment:
            // `.account` and `.region` will reflect the account+region the CLI
            // is configured to use (based on the user CLI credentials)
            new Stack(app, 'Stack2', {
              env: {
                account: process.env.CDK_DEFAULT_ACCOUNT,
                region: process.env.CDK_DEFAULT_REGION
              },
            });
            
            // Define multiple stacks stage associated with an environment
            const myStage = new Stage(app, 'MyStage', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              }
            });
            
            // both of these stacks will use the stage's account/region:
            // `.account` and `.region` will resolve to the concrete values as above
            new MyStack(myStage, 'Stack1');
            new YourStack(myStage, 'Stack2');
            
            // Define an environment-agnostic stack:
            // `.account` and `.region` will resolve to `{ "Ref": "AWS::AccountId" }` and `{ "Ref": "AWS::Region" }` respectively.
            // which will only resolve to actual values by CloudFormation during deployment.
            new MyStack(app, 'Stack1');
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Environment], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Name to deploy the stack with.

        :default: - Derived from construct path.
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synthesizer(self) -> typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer]:
        '''Synthesis method to use while deploying this stack.

        :default:

        - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag
        is set, ``LegacyStackSynthesizer`` otherwise.
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Stack tags that will be applied to all the taggable resources and the stack itself.

        :default: {}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable termination protection for this stack.

        :default: false
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stage(self) -> builtins.str:
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def new_relic_account_id(self) -> builtins.str:
        result = self._values.get("new_relic_account_id")
        assert result is not None, "Required property 'new_relic_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def new_relic_api_url_logs(self) -> EndpointUrlLogs:
        result = self._values.get("new_relic_api_url_logs")
        assert result is not None, "Required property 'new_relic_api_url_logs' is missing"
        return typing.cast(EndpointUrlLogs, result)

    @builtins.property
    def new_relic_api_url_metrics(self) -> EndpointUrlMetrics:
        result = self._values.get("new_relic_api_url_metrics")
        assert result is not None, "Required property 'new_relic_api_url_metrics' is missing"
        return typing.cast(EndpointUrlMetrics, result)

    @builtins.property
    def new_relic_bucket_name(self) -> builtins.str:
        result = self._values.get("new_relic_bucket_name")
        assert result is not None, "Required property 'new_relic_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def new_relic_license_key(self) -> builtins.str:
        result = self._values.get("new_relic_license_key")
        assert result is not None, "Required property 'new_relic_license_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NewRelicStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="neulabs-cdk-constructs.stacks.ProviderUrl")
class ProviderUrl(enum.Enum):
    GITHUB = "GITHUB"


@jsii.enum(jsii_type="neulabs-cdk-constructs.stacks.TokenActions")
class TokenActions(enum.Enum):
    ALL = "ALL"
    ALL_BRANCH = "ALL_BRANCH"
    ALL_TAGS = "ALL_TAGS"
    CUSTOM = "CUSTOM"


__all__ = [
    "BaseStack",
    "BaseStackProps",
    "EndpointType",
    "EndpointUrlLogs",
    "EndpointUrlMetrics",
    "GithubOIDCStack",
    "GithubOIDCStackStackProps",
    "NewRelicStack",
    "NewRelicStackProps",
    "ProviderUrl",
    "TokenActions",
]

publication.publish()

def _typecheckingstub__e8c3906f799f67d5a7e24ee1c0e82ba15bc0ee085154161fd98d129777139786(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    stage: builtins.str,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0c1253c5ad66fddcf1f03ca1661e0dcff75fd4de68d28896990299d9ee25bc(
    model: typing.Any,
    *,
    business_unit: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    repository_name: typing.Optional[builtins.str] = None,
    repository_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b9151b72dacaa74fd06951252aec9571e464b1e9decde23f52a407d018d0ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31847f9f18c83f9e0519164c5b05a3736c0afdc5714045805f62f54bf0f2a675(
    *,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
    stage: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2edd5d0fbd3812c3fe9c4b32c89e2358255a628a9b08ba813843df326922709d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    github_repository: builtins.str,
    github_user: builtins.str,
    token_action: TokenActions,
    cdk_deploy_role_managed_policies: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy]] = None,
    cdk_deploy_role_policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    token_action_custom: typing.Optional[builtins.str] = None,
    stage: builtins.str,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75edbe2b52327f605fc5a2ff70cc1370a8eacbbdb13d1db237f3dd4b9ee5c36a(
    managed_policies: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy]] = None,
    policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b14133f278789eb8e1e684f0c9a72082f2f8df9af6f48929c84547c5b70133f(
    provider_url: builtins.str,
    token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df3994aae471bf2921d73f61b727d533a660da9028b31a684c1d20a82a6cbef(
    token_action: TokenActions,
    github_user: builtins.str,
    github_repository: builtins.str,
    token_action_custom: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c045fafb37ff9100ec2a91b556074f24b5beceb07ea909463febe37129404d59(
    value: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7160e09388553b939314d9077e28ede6aab4965b51fca156dbced70bb51e1360(
    value: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87080802d68a6c0233ed49d6447901302ad8092daefae8287833b0fe17dfc683(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6642170ad325f27b7571dc1aaf9495313cdaa57532ee00e4c7c915196f8abb5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d4fbc01c038ea99e7305875f913ef979d93b13e57088b320555b4b1d5208e8(
    value: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03895cafb560af8d2a45fcda637206e2b68b92ede5263fa3e0238974b403e4fa(
    value: TokenActions,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4633d11a7f22626b7ed31e856302b0236ff8c5086b41ce88ecd332d21b20809(
    value: typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802ab8bfa128a99b9f73f4fb84580a1332025cf010c6902f197ca120289e2d4b(
    value: typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a443823344e7cbe6b0fd244775db3c260d3fff85df631e748d2ff85ad31f1fe(
    *,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
    stage: builtins.str,
    github_repository: builtins.str,
    github_user: builtins.str,
    token_action: TokenActions,
    cdk_deploy_role_managed_policies: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy]] = None,
    cdk_deploy_role_policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    token_action_custom: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66070d9b3140cc0a446c1ad3578a567763e44b80c35f76d1f1ad96cc4b946fb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    new_relic_account_id: builtins.str,
    new_relic_api_url_logs: EndpointUrlLogs,
    new_relic_api_url_metrics: EndpointUrlMetrics,
    new_relic_bucket_name: builtins.str,
    new_relic_license_key: builtins.str,
    stage: builtins.str,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99bce3b29be5c04fd361caab5cf05193a203e18b51f8401c627d9d1cbe985739(
    role_arn: builtins.str,
    firehose_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af065866a83d51eb0e0efade26989482a578f474975fbb0c354e6b35101cd54(
    new_relic_bucket_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7a7fa119bd27321fd2c372ff88c0e31f6399a8005d53db8ae1893206db7c83(
    new_relic_firehose_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba82381b3ec49fd57c738767405e96e64c27f63c6f7bcfd505efe3e141fa1274(
    new_relic_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
    endpoint_type: EndpointType,
    endpoint_url: builtins.str,
    new_relic_license_ley: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7305bbdc447fe35fa9f514bed3ae462d85bc16a0c458091c09de9a4e282c8539(
    new_relic_account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84c8a462bfc935cd2f4168debc558f4856a86d613033850469d399df40ccaaf(
    new_relic_account_id: builtins.str,
    new_relic_license_ley: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1acc91a446ee8b01943fd9805797d3ddeb6078e2b5c31fb8ac4b789382176ec(
    value: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ce2c39bb4a1970fceba0aeae62534edc819f3a962bc673fb639fa05ff48ff8(
    value: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8f4d498840b27542b7c21375598d3597d18f2825933afdd40cfff7f49f54ff(
    value: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ac8027091ea0e5a24b81302fdbf87847ed9ce182ee77c4e174286d7ce492c6(
    value: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9f75ef9eeacb91adae0e7c7a6a31805c523154e7854c5df972941469f6b723(
    value: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e9574b6c7d2bbbd95c0e93a31f3c1e665125256e90c5c4fe8ceacd450d74a85(
    value: typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb544dfdd2d81e3c5390d607beb842fecf8d5b037e4b42e634c845726be00d9(
    value: typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b7c9c4c2b943358cff93dc3eaf101b1711879fa1e3fc653e137feb6a4c418c(
    *,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
    stage: builtins.str,
    new_relic_account_id: builtins.str,
    new_relic_api_url_logs: EndpointUrlLogs,
    new_relic_api_url_metrics: EndpointUrlMetrics,
    new_relic_bucket_name: builtins.str,
    new_relic_license_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
