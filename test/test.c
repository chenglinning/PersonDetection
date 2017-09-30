#include <stdlib.h>
#include <stdio.h>
#include <string.h>
int main1111111111111()
{
        FILE *fp=fopen("../data/Image_Split_names.txt","r");
        if(fp==NULL)
        {
        printf("the file can not be opened\n");
        return 0;
        }
        while(!feof(fp)){
        char Inputfilename_tmp[256];
        char Outputfilename_tmp[256];
        fscanf(fp,"%s",Inputfilename_tmp);
        if(strcmp(Inputfilename_tmp,"Image_Split")==0)
        {break;}
        printf("%s\n",Inputfilename_tmp);
        char *filename=Inputfilename_tmp;
        //char *outfile = find_char_arg(argc, argv, "-out", 0);
        char *tmp=strtok(filename,"/");
        tmp=strtok(NULL,".");
        sprintf(Outputfilename_tmp,"results/%s",tmp);
        printf("%s\n",Outputfilename_tmp);
        }
        fclose(fp);
        return 0;
}


