namespace Calendar.Server.Application.Dtos.Team
{
    public class TeamDto
    {
        public long Id { get; set; }
        public string Name { get; set; }
        public string PrimaryColor { get; set; }
        public string SecondaryColor { get; set; }
        public bool Disabled { get; set; }
    }
}
