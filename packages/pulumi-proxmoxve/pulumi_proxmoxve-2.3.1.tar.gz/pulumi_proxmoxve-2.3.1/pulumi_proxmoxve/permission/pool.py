# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['PoolArgs', 'Pool']

@pulumi.input_type
class PoolArgs:
    def __init__(__self__, *,
                 pool_id: pulumi.Input[str],
                 comment: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Pool resource.
        :param pulumi.Input[str] pool_id: The pool id
        :param pulumi.Input[str] comment: The pool comment
        """
        pulumi.set(__self__, "pool_id", pool_id)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)

    @property
    @pulumi.getter(name="poolId")
    def pool_id(self) -> pulumi.Input[str]:
        """
        The pool id
        """
        return pulumi.get(self, "pool_id")

    @pool_id.setter
    def pool_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "pool_id", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        The pool comment
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)


@pulumi.input_type
class _PoolState:
    def __init__(__self__, *,
                 comment: Optional[pulumi.Input[str]] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input['PoolMemberArgs']]]] = None,
                 pool_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Pool resources.
        :param pulumi.Input[str] comment: The pool comment
        :param pulumi.Input[Sequence[pulumi.Input['PoolMemberArgs']]] members: The pool members
        :param pulumi.Input[str] pool_id: The pool id
        """
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if members is not None:
            pulumi.set(__self__, "members", members)
        if pool_id is not None:
            pulumi.set(__self__, "pool_id", pool_id)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        The pool comment
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def members(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PoolMemberArgs']]]]:
        """
        The pool members
        """
        return pulumi.get(self, "members")

    @members.setter
    def members(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PoolMemberArgs']]]]):
        pulumi.set(self, "members", value)

    @property
    @pulumi.getter(name="poolId")
    def pool_id(self) -> Optional[pulumi.Input[str]]:
        """
        The pool id
        """
        return pulumi.get(self, "pool_id")

    @pool_id.setter
    def pool_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pool_id", value)


class Pool(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 pool_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a Pool resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] comment: The pool comment
        :param pulumi.Input[str] pool_id: The pool id
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PoolArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a Pool resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param PoolArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PoolArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 pool_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PoolArgs.__new__(PoolArgs)

            __props__.__dict__["comment"] = comment
            if pool_id is None and not opts.urn:
                raise TypeError("Missing required property 'pool_id'")
            __props__.__dict__["pool_id"] = pool_id
            __props__.__dict__["members"] = None
        super(Pool, __self__).__init__(
            'proxmoxve:Permission/pool:Pool',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            comment: Optional[pulumi.Input[str]] = None,
            members: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PoolMemberArgs']]]]] = None,
            pool_id: Optional[pulumi.Input[str]] = None) -> 'Pool':
        """
        Get an existing Pool resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] comment: The pool comment
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PoolMemberArgs']]]] members: The pool members
        :param pulumi.Input[str] pool_id: The pool id
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PoolState.__new__(_PoolState)

        __props__.__dict__["comment"] = comment
        __props__.__dict__["members"] = members
        __props__.__dict__["pool_id"] = pool_id
        return Pool(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        """
        The pool comment
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter
    def members(self) -> pulumi.Output[Sequence['outputs.PoolMember']]:
        """
        The pool members
        """
        return pulumi.get(self, "members")

    @property
    @pulumi.getter(name="poolId")
    def pool_id(self) -> pulumi.Output[str]:
        """
        The pool id
        """
        return pulumi.get(self, "pool_id")

