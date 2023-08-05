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

__all__ = ['ClusterIPSetArgs', 'ClusterIPSet']

@pulumi.input_type
class ClusterIPSetArgs:
    def __init__(__self__, *,
                 cidrs: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterIPSetCidrArgs']]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ClusterIPSet resource.
        :param pulumi.Input[Sequence[pulumi.Input['ClusterIPSetCidrArgs']]] cidrs: List of IP or Networks
        :param pulumi.Input[str] comment: IPSet comment
        :param pulumi.Input[str] name: IPSet name
        """
        if cidrs is not None:
            pulumi.set(__self__, "cidrs", cidrs)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def cidrs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ClusterIPSetCidrArgs']]]]:
        """
        List of IP or Networks
        """
        return pulumi.get(self, "cidrs")

    @cidrs.setter
    def cidrs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterIPSetCidrArgs']]]]):
        pulumi.set(self, "cidrs", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        IPSet comment
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        IPSet name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ClusterIPSetState:
    def __init__(__self__, *,
                 cidrs: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterIPSetCidrArgs']]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ClusterIPSet resources.
        :param pulumi.Input[Sequence[pulumi.Input['ClusterIPSetCidrArgs']]] cidrs: List of IP or Networks
        :param pulumi.Input[str] comment: IPSet comment
        :param pulumi.Input[str] name: IPSet name
        """
        if cidrs is not None:
            pulumi.set(__self__, "cidrs", cidrs)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def cidrs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ClusterIPSetCidrArgs']]]]:
        """
        List of IP or Networks
        """
        return pulumi.get(self, "cidrs")

    @cidrs.setter
    def cidrs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterIPSetCidrArgs']]]]):
        pulumi.set(self, "cidrs", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        IPSet comment
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        IPSet name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class ClusterIPSet(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cidrs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterIPSetCidrArgs']]]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a ClusterIPSet resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterIPSetCidrArgs']]]] cidrs: List of IP or Networks
        :param pulumi.Input[str] comment: IPSet comment
        :param pulumi.Input[str] name: IPSet name
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ClusterIPSetArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a ClusterIPSet resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param ClusterIPSetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ClusterIPSetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cidrs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterIPSetCidrArgs']]]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClusterIPSetArgs.__new__(ClusterIPSetArgs)

            __props__.__dict__["cidrs"] = cidrs
            __props__.__dict__["comment"] = comment
            __props__.__dict__["name"] = name
        super(ClusterIPSet, __self__).__init__(
            'proxmoxve:Cluster/clusterIPSet:ClusterIPSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cidrs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterIPSetCidrArgs']]]]] = None,
            comment: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'ClusterIPSet':
        """
        Get an existing ClusterIPSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterIPSetCidrArgs']]]] cidrs: List of IP or Networks
        :param pulumi.Input[str] comment: IPSet comment
        :param pulumi.Input[str] name: IPSet name
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ClusterIPSetState.__new__(_ClusterIPSetState)

        __props__.__dict__["cidrs"] = cidrs
        __props__.__dict__["comment"] = comment
        __props__.__dict__["name"] = name
        return ClusterIPSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def cidrs(self) -> pulumi.Output[Optional[Sequence['outputs.ClusterIPSetCidr']]]:
        """
        List of IP or Networks
        """
        return pulumi.get(self, "cidrs")

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        """
        IPSet comment
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        IPSet name
        """
        return pulumi.get(self, "name")

