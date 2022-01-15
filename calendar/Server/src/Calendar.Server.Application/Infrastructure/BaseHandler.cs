using System;
using System.Data.Common;

namespace Calendar.Server.Application.Infrastructure
{
    public class BaseHandler :IDisposable
    {
        protected readonly DbConnection _db;

        public BaseHandler(ISqlSettings settings) =>
            _db = DatabaseExtension.CreateSqlConnection(settings);

        public void Dispose() =>
            _db.Close();
    }
}
