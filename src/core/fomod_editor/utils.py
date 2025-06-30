"""
Copyright (c) Cutleast
"""

from core.fomod.fomod import Fomod
from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod.module_config.plugin.plugin import Plugin
from core.utilities.unique import unique


class Utils:
    """
    Class with static utility methods for the FOMOD editor.
    """

    @staticmethod
    def get_fomod_flag_names(fomod: Fomod) -> list[str]:
        """
        Collects all mentioned flag names from the specified FOMOD installer.

        Args:
            fomod (Fomod): The FOMOD installer.

        Returns:
            list[str]: A list of all flag names mentioned in the FOMOD installer.
        """

        flag_names: list[str] = []

        if fomod.module_config.install_steps is not None:
            for install_step in fomod.module_config.install_steps.install_steps:
                if install_step.visible is not None:
                    flag_names.extend(
                        Utils.get_flag_names_from_composite_dependency(
                            install_step.visible.dependencies
                        )
                    )

                plugins: list[Plugin] = [
                    plugin
                    for group in install_step.optional_file_groups.groups
                    for plugin in group.plugins.plugins
                ]

                for plugin in plugins:
                    flag_names.extend(Utils.get_flag_names_from_plugin(plugin))

        if fomod.module_config.conditional_file_installs is not None:
            for (
                pattern
            ) in fomod.module_config.conditional_file_installs.patterns.patterns:
                flag_names.extend(
                    Utils.get_flag_names_from_composite_dependency(pattern.dependencies)
                )

        return unique(sorted(flag_names))

    @staticmethod
    def get_flag_names_from_composite_dependency(
        composite_dependency: CompositeDependency,
    ) -> list[str]:
        """
        Collects all mentioned flag names from the specified composite dependency.

        Args:
            composite_dependency (CompositeDependency): The composite dependency.

        Returns:
            list[str]: A list of all flag names mentioned in the composite dependency.
        """

        flag_names: list[str] = [
            dep.flag for dep in composite_dependency.flag_dependencies
        ]

        for dep in composite_dependency.dependencies:
            flag_names.extend(Utils.get_flag_names_from_composite_dependency(dep))

        return unique(sorted(flag_names))

    @staticmethod
    def get_flag_names_from_plugin(plugin: Plugin) -> list[str]:
        """
        Collects all mentioned flag names from the specified plugin.

        Args:
            plugin (Plugin): The plugin.

        Returns:
            list[str]: A list of all flag names mentioned in the plugin.
        """

        flag_names: list[str] = []

        if plugin.type_descriptor.dependency_type is not None:
            for dep in plugin.type_descriptor.dependency_type.patterns.patterns:
                flag_names.extend(
                    Utils.get_flag_names_from_composite_dependency(dep.dependencies)
                )

        if plugin.condition_flags is not None:
            flag_names.extend(flag.name for flag in plugin.condition_flags.flags)

        return unique(sorted(flag_names))
