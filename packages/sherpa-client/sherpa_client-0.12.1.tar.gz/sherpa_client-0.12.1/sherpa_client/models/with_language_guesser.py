from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.apply_to import ApplyTo
    from ..models.depends_on import DependsOn
    from ..models.next_step import NextStep
    from ..models.with_language_guesser_condition import WithLanguageGuesserCondition
    from ..models.with_language_guesser_parameters import WithLanguageGuesserParameters


T = TypeVar("T", bound="WithLanguageGuesser")


@attr.s(auto_attribs=True)
class WithLanguageGuesser:
    """
    Attributes:
        language_guesser (str):
        apply_to (Union[Unset, ApplyTo]):
        condition (Union[Unset, WithLanguageGuesserCondition]):
        depends_on (Union[Unset, DependsOn]):
        disabled (Union[Unset, bool]):
        group (Union[Unset, str]):
        id (Union[Unset, str]):
        next_steps (Union[Unset, List['NextStep']]):
        parameters (Union[Unset, WithLanguageGuesserParameters]):
        project_name (Union[Unset, str]):
    """

    language_guesser: str
    apply_to: Union[Unset, "ApplyTo"] = UNSET
    condition: Union[Unset, "WithLanguageGuesserCondition"] = UNSET
    depends_on: Union[Unset, "DependsOn"] = UNSET
    disabled: Union[Unset, bool] = UNSET
    group: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    next_steps: Union[Unset, List["NextStep"]] = UNSET
    parameters: Union[Unset, "WithLanguageGuesserParameters"] = UNSET
    project_name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        language_guesser = self.language_guesser
        apply_to: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.apply_to, Unset):
            apply_to = self.apply_to.to_dict()

        condition: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.condition, Unset):
            condition = self.condition.to_dict()

        depends_on: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.depends_on, Unset):
            depends_on = self.depends_on.to_dict()

        disabled = self.disabled
        group = self.group
        id = self.id
        next_steps: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.next_steps, Unset):
            next_steps = []
            for next_steps_item_data in self.next_steps:
                next_steps_item = next_steps_item_data.to_dict()

                next_steps.append(next_steps_item)

        parameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        project_name = self.project_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "languageGuesser": language_guesser,
            }
        )
        if apply_to is not UNSET:
            field_dict["applyTo"] = apply_to
        if condition is not UNSET:
            field_dict["condition"] = condition
        if depends_on is not UNSET:
            field_dict["dependsOn"] = depends_on
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if group is not UNSET:
            field_dict["group"] = group
        if id is not UNSET:
            field_dict["id"] = id
        if next_steps is not UNSET:
            field_dict["nextSteps"] = next_steps
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if project_name is not UNSET:
            field_dict["projectName"] = project_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.apply_to import ApplyTo
        from ..models.depends_on import DependsOn
        from ..models.next_step import NextStep
        from ..models.with_language_guesser_condition import WithLanguageGuesserCondition
        from ..models.with_language_guesser_parameters import WithLanguageGuesserParameters

        d = src_dict.copy()
        language_guesser = d.pop("languageGuesser")

        _apply_to = d.pop("applyTo", UNSET)
        apply_to: Union[Unset, ApplyTo]
        if isinstance(_apply_to, Unset):
            apply_to = UNSET
        else:
            apply_to = ApplyTo.from_dict(_apply_to)

        _condition = d.pop("condition", UNSET)
        condition: Union[Unset, WithLanguageGuesserCondition]
        if isinstance(_condition, Unset):
            condition = UNSET
        else:
            condition = WithLanguageGuesserCondition.from_dict(_condition)

        _depends_on = d.pop("dependsOn", UNSET)
        depends_on: Union[Unset, DependsOn]
        if isinstance(_depends_on, Unset):
            depends_on = UNSET
        else:
            depends_on = DependsOn.from_dict(_depends_on)

        disabled = d.pop("disabled", UNSET)

        group = d.pop("group", UNSET)

        id = d.pop("id", UNSET)

        next_steps = []
        _next_steps = d.pop("nextSteps", UNSET)
        for next_steps_item_data in _next_steps or []:
            next_steps_item = NextStep.from_dict(next_steps_item_data)

            next_steps.append(next_steps_item)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, WithLanguageGuesserParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = WithLanguageGuesserParameters.from_dict(_parameters)

        project_name = d.pop("projectName", UNSET)

        with_language_guesser = cls(
            language_guesser=language_guesser,
            apply_to=apply_to,
            condition=condition,
            depends_on=depends_on,
            disabled=disabled,
            group=group,
            id=id,
            next_steps=next_steps,
            parameters=parameters,
            project_name=project_name,
        )

        return with_language_guesser
