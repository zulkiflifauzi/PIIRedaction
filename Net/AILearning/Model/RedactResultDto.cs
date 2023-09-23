namespace AILearning.Model
{
    public class RedactResultDto
    {
        public string entity_type { get; set; }
        public string value { get; set;}
        public double start { get; set;}
        public double end { get; set; }
        public double score { get; set; }
    }
}
