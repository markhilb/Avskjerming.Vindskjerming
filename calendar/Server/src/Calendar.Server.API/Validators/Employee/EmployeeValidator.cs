using Calendar.Server.Application.Dtos.Employee;
using FluentValidation;

public class EmployeeValidator : AbstractValidator<EmployeeDto>
{
    public EmployeeValidator()
    {
        RuleFor(x => x.Name).MaximumLength(255).WithMessage("Navn kan ha max 255 karakterer");
        RuleFor(x => x.Color).MaximumLength(9).WithMessage("Farge kan ha max 9 karakterer");
    }
}
