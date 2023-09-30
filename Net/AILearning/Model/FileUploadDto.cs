﻿namespace AILearning.Model
{
    public class SaveFileDto
    {
        public SaveFileDto()
        {
            Files = new List<FileDataDto>();
        }
        public List<FileDataDto> Files { get; set; }
    }

    public class FileDataDto
    {
        public byte[] ImageBytes { get; set; }
        public string FileName { get; set; }
        public string FileType { get; set; }
        public long FileSize { get; set; }
    }
}
