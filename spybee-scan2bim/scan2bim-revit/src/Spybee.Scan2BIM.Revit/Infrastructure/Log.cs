using System;
using System.Globalization;
using System.IO;

namespace Spybee.Scan2BIM.Revit.Infrastructure
{
    /// <summary>
    /// Minimal file logger: %LOCALAPPDATA%\Spybee\Scan2BIM\logs\scan2bim-yyyyMMdd.log.
    /// Never throws (logging must not break a Revit command).
    /// </summary>
    internal static class Log
    {
        private static readonly object Gate = new object();

        public static string Folder => Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Spybee", "Scan2BIM", "logs");

        public static void Info(string message) => Write("INFO", message);

        public static void Warn(string message) => Write("WARN", message);

        public static void Error(string message, Exception? ex = null) =>
            Write("ERROR", ex == null ? message : $"{message}{Environment.NewLine}{ex}");

        private static void Write(string level, string message)
        {
            try
            {
                lock (Gate)
                {
                    Directory.CreateDirectory(Folder);
                    string file = Path.Combine(Folder, $"scan2bim-{DateTime.Now.ToString("yyyyMMdd", CultureInfo.InvariantCulture)}.log");
                    string line = $"{DateTime.Now.ToString("HH:mm:ss", CultureInfo.InvariantCulture)} {level,-5} {message}{Environment.NewLine}";
                    File.AppendAllText(file, line);
                }
            }
            catch (IOException)
            {
                // ignore: logging is best effort
            }
            catch (UnauthorizedAccessException)
            {
                // ignore: logging is best effort
            }
        }
    }
}
