using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UglyToad.PdfPig;

namespace AIManager
{
    internal class TextProcessing
    {
        public string ExtracrTextFromPdf(string filePath)
        {
            using var pdf = PdfDocument.Open(filePath);
            var sb = new StringBuilder();
            foreach (var page in pdf.GetPages())
            {
                sb.Append(page.Text);
            }
            return sb.ToString();
        }

        public List<string> SplitTextIntoChunksWithOverlap(string text, int chunkSize, int overlapSize)
        {
            var words = text.Split(' ');
            var chunks = new List<string>();

            for (int i = 0; i < words.Length; i += chunkSize - overlapSize)
            {
                var chunkWords = words.Skip(i).Take(chunkSize).ToArray();
                var chunk = string.Join(" ", chunkWords);
                chunks.Add(chunk);
            }

            return chunks;
        }

        public List<string> SplitFileIntoChunksWithOverlap(string filePath, int chunkSize, int overlapSize)
        {
            string content = ExtracrTextFromPdf(filePath);
            return SplitTextIntoChunksWithOverlap(content, chunkSize, overlapSize);            
        }
    }
}
