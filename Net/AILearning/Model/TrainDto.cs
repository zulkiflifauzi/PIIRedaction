namespace AILearning.Model
{
    public class TrainDto
    {
        public string FileName { get; set; }
        public string Sentence { get; set; }
        public List<string> Labels { get; set; }
    }
}
