using Newtonsoft.Json;

namespace AILearning.Helper
{
    public static class Helper
    {
        public static string Dump<T>(this T obj, bool indent = false)
        {
            return JsonConvert.SerializeObject(obj, indent ? Formatting.Indented : Formatting.None,
                new JsonSerializerSettings { NullValueHandling = NullValueHandling.Ignore });
        }
    }
}
