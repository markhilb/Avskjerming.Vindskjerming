using Calendar.Server.Application.Dtos.Team;
using FluentValidation;

public class TeamValidator : AbstractValidator<TeamDto>
{
    public TeamValidator()
    {
        RuleFor(x => x.Name).MaximumLength(255).WithMessage("Navn kan ha max 255 karakterer");
        RuleFor(x => x.PrimaryColor).MaximumLength(9).WithMessage("Hoved farge kan ha max 9 karakterer");
        RuleFor(x => x.SecondaryColor).MaximumLength(9).WithMessage("Andre farge kan ha max 9 karakterer");
    }
}
