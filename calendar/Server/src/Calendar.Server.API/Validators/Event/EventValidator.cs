using Calendar.Server.Application.Dtos.Event;
using FluentValidation;

public class EventValidator : AbstractValidator<EventDto>
{
    public EventValidator()
    {
        RuleFor(x => x.Title).MaximumLength(255).WithMessage("Tittel kan ha max 255 karakterer");
        RuleFor(x => x.Details).MaximumLength(255).WithMessage("Detailjer kan ha max 255 karakterer");
        RuleFor(x => x.End).GreaterThan(x => x.Start).WithMessage("Slutt dato må være etter start dato");
    }
}
