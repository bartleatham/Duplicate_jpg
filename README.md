# Duplicate_jpg
this script will identify the year/month a .jpg image was created using exif metadata.  The image will be moved to a directory \<path\>/year/month, where <\path\> is input from user and created if it does not exist.
The script then identifies any duplicate files in the new directory tree and renames them with _DUP so that the user can easily find and remove them if they wish.
TODO:
1-Test on larger data sets to discover bugs/exceptions
2-if exif metadata does not exist, move image to \<path\>/no_date
2-add ability to batch remove all _DUP files at script invocation.
