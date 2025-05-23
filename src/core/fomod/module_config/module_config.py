"""
Copyright (c) Cutleast
"""

from typing import Optional, override

from pydantic_xml import element

from ..fomod_model import FomodModel
from .condition.conditional_file_install_list import ConditionalFileInstallList
from .dependency.composite_dependency import CompositeDependency
from .file_list import FileList
from .header_image import HeaderImage
from .module_title import ModuleTitle
from .step_list import StepList


class ModuleConfig(FomodModel, tag="config", search_mode="unordered"):
    """
    Model representing the ModuleConfig.xml file of a FOMOD installer.

    Describes the configuration of a module.
    """

    module_name: ModuleTitle = element(tag="moduleName")
    """The name of the module."""

    header_image: Optional[HeaderImage] = element(tag="moduleImage", default=None)
    """The module logo."""

    module_dependencies: list[CompositeDependency] = element(
        tag="moduleDependencies", default_factory=list
    )
    """Items upon which the module depends."""

    required_install_files: FileList = element(
        tag="requiredInstallFiles",
        default_factory=lambda: FileList(files=[], folders=[]),
    )
    """The list of files and folders that must be installed for this module."""

    install_steps: StepList = element(
        tag="installSteps", default_factory=lambda: StepList(install_steps=[])
    )
    """
    The list of install steps that determine which files (or plugins) that may optionally
    be installed for this module.
    """

    conditional_file_installs: ConditionalFileInstallList = element(
        tag="conditionalFileInstalls",
        default_factory=lambda: ConditionalFileInstallList(patterns=[]),
    )
    """
    The list of optional files that may optionally be installed for this module, based on
    condition flags.
    """

    @override
    @classmethod
    def get_schema_url(cls) -> str:
        return "https://raw.githubusercontent.com/Cutleast/FOMOD-Creation-Kit/master/res/schemas/ModuleConfig.xsd"
