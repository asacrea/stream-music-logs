import boto3
import cfnresponse

def lambda_handler(event, context):
    '''
    This functions create each folder we use to develop door2door project
    '''
    the_event= event["RequestType"]
    print("The event is: ",  str(the_event))
    response_data = {}
    s3 = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    #Retrieve parameters
    the_bucket = event['ResourceProperties']['the_bucket']
    dirs_to_create = event['ResourceProperties']['dirs_to_create']

    try:
        if the_event in ('Create', 'Update'):
            print("Request folder:", str(dirs_to_create).split(","))
            for dir_name in str(dirs_to_create).split(","):
                print('Creating: ', str(dir_name))
                s3.put_object(Bucket=the_bucket,
                              Key=(dir_name
                                 + '/'))
              
        elif the_event == 'Delete':
            print("Deleting S3 content...")
            bucket = s3_resource.Bucket(the_bucket)
            bucket.objects.all().delete()
            print("All objects deleted")
            bucket.object_version.delete()
            print("All object version deleted")
            s3.delete_bucket(Bucket=str(the_bucket))
            print("Bucket deleted")
        print("Executeion successful")
        cfnresponse.send(event,
                         context,
                         cfnresponse.SUCCESS,
                         response_data)
    except Exception as e:
        print("Execution failed...")
        print(str(e))
        response_data['Data'] = str(e)
        cfnresponse.send(event,
                         context,
                         cfnresponse.FAILED,
                         response_data)