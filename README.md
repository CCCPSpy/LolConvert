# LolConvert

Convert League of Legends replay files from webm format to MP4. This will put a copy of the MP4 into the "output" filder and then upload it to Azure blob storage. This will also work for any file that ffmpeg could conver to MP4.

### Requirements:
- ffmpeg.exe in the same directory.
- Create a .env file with your Azure Stroage account secrets.
- Have an Azure Storage account with a blob container created.
- If you would like to share the links the blob container will need to be set to public.

### How to use:
Execute convert.py and provide two arguments. First the input webm path and then the name of the coverted MP4 filename.

### Example:
```
python convert.py 10-16_NA1-3554167066_04.webm Pentakill.mp4
```
