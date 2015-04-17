int main()
{
    int a[10];
    int i;
    int sum;
    for(i=0; i< 10; i++)
    {
        scanf(" %s",&a[i]);
    }
    sum = 0;
    for(i=0; i< 10; i++)
    {
        sum = sum + a[i];
    }
    printf("Avg: %f", sum*1.0/10);
    return 0;
}
