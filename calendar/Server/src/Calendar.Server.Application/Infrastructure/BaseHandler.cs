using System;
using System.Data.Common;
using System.Security.Cryptography;
using System.Text;

namespace Calendar.Server.Application.Infrastructure
{
    public class BaseHandler : IDisposable
    {
        protected readonly DbConnection _db;

        public BaseHandler(ISqlSettings settings) =>
            _db = DatabaseExtension.CreateSqlConnection(settings);

        public void Dispose() =>
            _db.Close();

        public static string ComputeSHA256Hash(string input)
        {
            var bytes = SHA256.Create().ComputeHash(Encoding.ASCII.GetBytes("qGmLwByUv_" + input));

            var result = new StringBuilder();
            for (int i = 0; i < bytes.Length; i++)
                result.Append(bytes[i].ToString("x2"));

            return result.ToString();
        }
    }
}
