namespace Calendar.Server.Application.Dtos.Authentication
{
    public class ChangePasswordDto
    {
        public string OldPassword { get; set; }
        public string NewPassword { get; set; }
    }
}
