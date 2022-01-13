using System.Data.Common;

namespace Calendar.Server.Application.Infrastructure
{
    public class BaseHandler
    {
        protected readonly DbConnection _db;

        public BaseHandler(DbConnection db) => _db = db;
    }
}
