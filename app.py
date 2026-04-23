import argparse
from main import S3Manager 



def main():
    parser = argparse.ArgumentParser(description="S3 CLI Tool")

    subparsers = parser.add_subparsers(dest="command")

    # CREATE
    create = subparsers.add_parser("create")
    create.add_argument("bucket_name")

    #Upload
    upload = subparsers.add_parser("upload")
    upload.add_argument("bucket_name")
    upload.add_argument("file_path")
    upload.add_argument("key")

    #put bucket configuration
    putconfiguration = subparsers.add_parser("putconfiguration")
    putconfiguration.add_argument("bucket_name")

    #get bucket configuration
    getconfiguration = subparsers.add_parser("getconfiguration")
    getconfiguration.add_argument("bucket_name")

    # put bucket policy
    putpolicy = subparsers.add_parser("putpolicy")
    putpolicy.add_argument("bucket_name")

    # get bucket policy
    getpolicy = subparsers.add_parser("getpolicy")
    getpolicy.add_argument("bucket_name")

    # Download file from S3 bucket 
    download = subparsers.add_parser("download")
    download.add_argument("bucket_name")
    download.add_argument("key")
    download.add_argument("local_file_path")

    # set versioning
    versioning = subparsers.add_parser("versioning")
    versioning.add_argument("bucket_name")
    versioning.add_argument("enable")

    

    # delete object
    deleteobject = subparsers.add_parser("deleteobject")
    deleteobject.add_argument("bucket_name")
    deleteobject.add_argument("key")
    

    # empty_and_delete_bucket
    deletebucket = subparsers.add_parser("deletebucket")
    deletebucket.add_argument("bucket_name")

    # LIST
    list_cmd = subparsers.add_parser("list")
    list_cmd.add_argument("bucket_name")
    list_cmd.add_argument("--prefix", default=None)

    # listversions
    listversions = subparsers.add_parser("listversions")
    listversions.add_argument("bucket_name")
    listversions.add_argument("--prefix", default=None)

    



    args = parser.parse_args()

    manager = S3Manager()

    if args.command == "create":
        manager.create_bucket(args.bucket_name)

    elif args.command == "upload":
        manager.upload(args.bucket_name,args.file_path, args.key)

    elif args.command == "putconfiguration":
        manager.put_bucket_config(args.bucket_name)

    elif args.command == "getconfiguration":
        manager.get_bucket_config(args.bucket_name)    
    
    elif args.command == "putpolicy":
        manager.put_bucket_policy(args.bucket_name)

    elif args.command == "getpolicy":
        manager.get_bucket_policy(args.bucket_name)

    elif args.command == "versioning":
        enable = args.enable.lower() == "true"
        manager.set_versioning(
            args.bucket_name,
            enable=enable
    )

    elif args.command == "download":
        manager.download_object_from_s3(args.bucket_name,args.key, args.local_file_path)

    elif args.command == "deleteobject":
        manager.delete_object(args.bucket_name,  args.key)


    elif args.command == "deletebucket":
        manager.empty_and_delete_bucket(args.bucket_name)

    elif args.command == "list":
        manager.list_objects(args.bucket_name,prefix=args.prefix)

    elif args.command == "listversions":
        manager.list_object_versions(args.bucket_name, prefix=args.prefix)


if __name__ == "__main__":
    main()