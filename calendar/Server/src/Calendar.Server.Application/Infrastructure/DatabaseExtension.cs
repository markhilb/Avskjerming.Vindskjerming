using System.Data.Common;
using System.Data.SqlClient;

namespace Calendar.Server.Application.Infrastructure
{
    public static class DatabaseExtension
    {
        public static DbConnection CreateSqlConnection(ISqlSettings settings)
        {
            var connection = new SqlConnection(settings.ConnectionString);
            connection.Open();
            return connection;
        }
    }
}
