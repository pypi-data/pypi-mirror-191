"""
The HEA Server AWS Accounts Microservice provides ...
"""
import logging
from asyncio import gather
from heaserver.service.heaobjectsupport import type_to_resource_url
from heaserver.service.oidcclaimhdrs import SUB
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import awsservicelib, aws
from heaserver.service.wstl import builder_factory, action
from heaserver.service import response, client
from heaobject.bucket import AWSBucket
from heaobject.storage import AWSStorage
from heaobject.folder import AWSS3BucketItem
from heaobject.root import DesktopObjectDict
from heaobject.volume import AWSFileSystem
from yarl import URL
from aiohttp import hdrs


@routes.get('/ping')
async def ping(request: web.Request) -> web.Response:
    """
    For testing whether the service is up.

    :param request: the HTTP request.
    :return: Always returns status code 200.
    """
    return response.status_ok(None)


@routes.get('/awsaccounts/{id}')
@action('heaserver-accounts-awsaccount-get-open-choices', rel='hea-opener-choices hea-context-menu', path='/awsaccounts/{id}/opener')
@action('heaserver-accounts-awsaccount-get-properties', rel='hea-properties hea-context-menu')
@action('heaserver-accounts-awsaccount-get-create-choices', rel='hea-creator-choices hea-context-menu', path='/awsaccounts/{id}/creator')
@action('heaserver-accounts-awsaccount-get-self', rel='self hea-account', path='/awsaccounts/{id}')
@action(name='heaserver-accounts-awsaccount-get-volume', rel='hea-volume', path='/volumes/{volume_id}')
async def get_awsaccount(request: web.Request) -> web.Response:
    """
    Gets the AWS account with the given id. IIf no AWS credentials can be found, it uses any credentials found by the
    AWS boto3 library.

    :param request: the HTTP request.
    :return: a Response object with the requested AWS account or Not Found.
    ---
    summary: The user's AWS account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    account_dict, volume_id = await awsservicelib.get_account_by_id(request)
    request.match_info['volume_id'] = volume_id
    return await response.get(request, account_dict)


@routes.get('/awsaccounts')
@routes.get('/awsaccounts/')
@action('heaserver-accounts-awsaccount-get-open-choices', rel='hea-opener-choices hea-context-menu', path='/awsaccounts/{id}/opener')
@action('heaserver-accounts-awsaccount-get-properties', rel='hea-properties hea-context-menu')
@action('heaserver-accounts-awsaccount-get-create-choices', rel='hea-creator-choices hea-context-menu', path='/awsaccounts/{id}/creator')
@action('heaserver-accounts-awsaccount-get-self', rel='self', path='/awsaccounts/{id}')
async def get_awsaccounts(request: web.Request) -> web.Response:
    """
    Gets all AWS accounts. If no AWS credentials can be found, it uses any credentials found by the AWS boto3 library.

    :param request: the HTTP request.
    :return: a Response object with the requested AWS accounts or the empty list
    ---
    summary: The user's AWS accounts.
    tags:
        - heaserver-accounts-awsaccount
    responses:
      '200':
        $ref: '#/components/responses/200'
    """
    aws_account_dicts = await awsservicelib.get_all_accounts(request)
    return await response.get_all(request, aws_account_dicts)


@routes.get('/volumes/{volume_id}/awsaccounts/me')
@action('heaserver-accounts-awsaccount-get-open-choices', rel='hea-opener-choices hea-context-menu',
        path='/volumes/{volume_id}/awsaccounts/me/opener')
@action('heaserver-accounts-awsaccount-get-properties', rel='hea-properties hea-context-menu')
@action('heaserver-accounts-awsaccount-get-create-choices', rel='hea-creator-choices hea-context-menu', path='/awsaccounts/{id}/creator')
@action('heaserver-accounts-awsaccount-get-self', rel='self hea-account', path='/awsaccounts/{id}')
@action(name='heaserver-accounts-awsaccount-get-volume', rel='hea-volume', path='/volumes/{volume_id}')
async def get_awsaccount_by_volume_id(request: web.Request) -> web.Response:
    """
    Gets the AWS account associated with the given volume id. If the volume's credentials are None, it uses any
    credentials found by the AWS boto3 library.

    :param request: the HTTP request.
    :return: the requested AWS account or Not Found.
    ---
    summary: The user's AWS account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_account(request, request.match_info["volume_id"])


@routes.get('/awsaccounts/{id}/opener')
@action('heaserver-accounts-awsaccount-open-buckets',
        rel=f'hea-opener hea-context-aws hea-default {AWSBucket.get_mime_type()}', path='/volumes/{volume_id}/awsaccounts/me/bucketitems/')
@action('heaserver-accounts-awsaccount-open-storage',
        rel=f'hea-opener hea-context-aws {AWSStorage.get_mime_type()}', path='/volumes/{volume_id}/storage/')
async def get_awsaccount_opener(request: web.Request) -> web.Response:
    """
    Gets choices for opening an AWS account.

    :param request: the HTTP Request.
    :return: A Response object with a status of Multiple Choices or Not Found.
    ---
    summary: AWS account opener choices
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    volume_id = await awsservicelib.get_volume_id_for_account_id(request)
    request.match_info['volume_id'] = volume_id  # Needed to make the action work.
    return await awsservicelib.account_opener(request, volume_id)


@routes.get('/volumes/{volume_id}/awsaccounts/me/bucketitems')
@routes.get('/volumes/{volume_id}/awsaccounts/me/bucketitems/')
@action('heaserver-accounts-bucket-get-self', rel='self', path='/volumes/{volume_id}/buckets/{id}')
async def get_buckets_by_volume_id(request: web.Request) -> web.Response:
    """
    Gets the S3 bucket items in the provided account.

    :param request: the HTTP Request.
    :return: a Response object with status code 200 and a body containing either an empty list or a list of buckets.
    ---
    summary: the buckets in an AWS account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
        '200':
            $ref: '#/components/responses/200'
    """
    logging.debug("Getting volume id by account id")

    headers = {SUB: request.headers.get(SUB),
               hdrs.AUTHORIZATION: request.headers.get(hdrs.AUTHORIZATION, '')} if SUB in request.headers else None
    volume_id = request.match_info['volume_id']
    if volume_id is None:
        logging.debug("Volume id was not found")
        bucket_dicts = []
    else:
        resource_url_str = await type_to_resource_url(request=request, type_or_type_name=AWSS3BucketItem,
                                             file_system_type_or_type_name=AWSFileSystem)
        url = URL(resource_url_str) / volume_id / 'bucketitems'

        async def get_one_bucket_dict(b: AWSS3BucketItem) -> DesktopObjectDict:
            logging.info("Bucket names  %s returning", b.display_name)
            return b.to_dict()
        bucket_dicts = await gather(*[get_one_bucket_dict(b) async for b in
                                      client.get_all(app=request.app, url=url, type_=AWSS3BucketItem, headers=headers)])

    return await response.get_all(request, bucket_dicts)


@routes.get('/awsaccounts/{id}/buckets')
@routes.get('/awsaccounts/{id}/buckets/')
@action('heaserver-accounts-bucket-get-self', rel='self', path='/volumes/{volume_id}/buckets/{id}')
async def get_buckets(request: web.Request) -> web.Response:
    """
    Gets the S3 bucket items in the provided account.

    :param request: the HTTP Request.
    :return: a Response object with status code 200 and a body containing either an empty list or a list of buckets.
    ---
    summary: the buckets in an AWS account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
        '200':
            $ref: '#/components/responses/200'
    """
    logging.debug("Getting volume id by account id")

    headers = {SUB: request.headers.get(SUB),
               hdrs.AUTHORIZATION: request.headers.get(hdrs.AUTHORIZATION, '')} if SUB in request.headers else None
    id = request.match_info.get('id')
    if not id:
        return response.status_bad_request('id is required')
    volume_id = await awsservicelib.get_volume_id_for_account_id(id)
    if volume_id is None:
        return response.status_bad_request(f'Invalid id {id}')
    else:
        url = URL(await type_to_resource_url(request=request, type_or_type_name=AWSS3BucketItem,
                                             file_system_type_or_type_name=AWSFileSystem)) / volume_id / 'buckets'

        async def get_one_bucket_dict(b: AWSS3BucketItem) -> DesktopObjectDict:
            logging.info("Bucket names  %s returning", b.display_name)
            return b.to_dict()
        bucket_dicts = await gather(*[get_one_bucket_dict(b) async for b in
                                      client.get_all(app=request.app, url=url, type_=AWSS3BucketItem, headers=headers)])
        request.match_info['volume_id'] = volume_id
        return await response.get_all(request, bucket_dicts)


@routes.get('/volumes/{volume_id}/awsaccounts/me/opener')
@action('heaserver-accounts-awsaccount-open-buckets',
        rel=f'hea-opener hea-context-aws hea-default {AWSBucket.get_mime_type()}', path='/volumes/{volume_id}/bucketitems/')
@action('heaserver-accounts-awsaccount-open-storage',
        rel=f'hea-opener hea-context-aws {AWSStorage.get_mime_type()}', path='/volumes/{volume_id}/storage/')
async def get_awsaccount_opener_by_volume_id(request: web.Request) -> web.Response:
    """
    Gets choices for opening an AWS account.

    :param request: the HTTP Request.
    :return: A Response object with a status of Multiple Choices or Not Found.
    ---
    summary: AWS account opener choices
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.account_opener(request, request.match_info['volume_id'])


@routes.post('/volumes/{volume_id}/awsaccounts/me')
async def post_account_awsaccounts(request: web.Request) -> web.Response:
    """
    Posts the awsaccounts information given the correct access key and secret access key.

    :param request: the HTTP request.
    :return: the requested awsaccounts or Not Found.

    FIXME: should only be permitted by an AWS organization administrator, I would think. Need to sort out what the call looks like.
    """
    return await awsservicelib.post_account(request)


@routes.put('/volumes/{volume_id}/awsaccounts/me')
async def put_account_awsaccounts(request: web.Request) -> web.Response:
    """
    Puts the awsaccounts information given the correct access key and secret access key.

    :param request: the HTTP request.
    :return: the requested awsaccounts or Not Found.
    """
    return await awsservicelib.put_account(request)


@routes.delete('/volumes/{volume_id}/awsaccounts/me')
async def delete_account_awsaccounts(request: web.Request) -> web.Response:
    """
    Deletes the awsaccounts information given the correct access key and secret access key.

    :param request: the HTTP request.
    :return: the requested awsaccounts or Not Found.

    FIXME: should only be permitted by an AWS organization administrator, I would think. Need to sort out what the call looks like.
    """
    return await awsservicelib.delete_account(request, request.match_info["volume_id"])


@routes.get('/awsaccounts/{id}/creator')
@action('heaserver-accounts-awsaccount-create-bucket', rel='hea-creator hea-default application/x.bucket',
        path='/awsaccounts/{id}/newbucket')
async def get_account_creator(request: web.Request) -> web.Response:
    """
        Gets account creator choices.

        :param request: the HTTP Request.
        :return: A Response object with a status of Multiple Choices or Not Found.
        ---
        summary: Account creator choices
        tags:
            - heaserver-accounts-awsaccount
        parameters:
            - $ref: '#/components/parameters/id'
        responses:
          '300':
            $ref: '#/components/responses/300'
          '404':
            $ref: '#/components/responses/404'
        """
    return await awsservicelib.account_opener_by_id(request)


@routes.get('/volumes/{volume_id}/awsaccounts/me/creator')
@action('heaserver-accounts-awsaccount-create-bucket', rel='hea-creator hea-default application/x.bucket',
        path='/volumes/{volume_id}/awsaccounts/me/newbucket')
async def get_account_creator_by_volume_id(request: web.Request) -> web.Response:
    """
    Gets account creator choices.

    :param request: the HTTP Request.
    :return: A Response object with a status of Multiple Choices or Not Found.
    ---
    summary: Account creator choices
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - $ref: '#/components/parameters/id'
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.account_opener(request, request.match_info["volume_id"])


@routes.get('/volumes/{volume_id}/awsaccounts/me/newbucket')
@routes.get('/volumes/{volume_id}/awsaccounts/me/newbucket/')
@action('heaserver-accounts-awsaccount-new-bucket-form')
async def get_new_bucket_form_by_volume_id(request: web.Request) -> web.Response:
    """
    Gets form for creating a new bucket in this account.

    :param request: the HTTP request. Required.
    :return: the current bucket, with a template for creating a child folder or Not Found if the requested item does not
    exist.
    ---
    summary: An account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_account(request, request.match_info["volume_id"])


@routes.post('/volumes/{volume_id}/awsaccounts/me/newbucket')
@routes.post('/volumes/{volume_id}/awsaccounts/me/newbucket/')
async def post_new_bucket_by_volume_id(request: web.Request) -> web.Response:
    """
    Gets form for creating a new bucket in this account.

    :param request: the HTTP request. Required.
    :return: the current account, with a template for creating a bucket or Not Found if the requested account does not
    exist.
    ---
    summary: An account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    requestBody:
        description: A new bucket.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: Folder example
                  value: {
                    "template": {
                      "data": [
                      {
                        "name": "display_name",
                        "value": "my-bucket"
                      },
                      {
                        "name": "type",
                        "value": "heaobject.bucket.AWSBucket"
                      },
                      {
                        "name": "region",
                        "value": "us-west-1"
                      }]
                    }
                  }
            application/json:
              schema:
                type: object
              examples:
                example:
                  summary: Item example
                  value: {
                    "display_name": "my-bucket",
                    "type": "heaobject.bucket.AWSBucket",
                    "region": "us-west-1"
                  }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.post_bucket(request)


@routes.get('/awsaccounts/{id}/newbucket')
@routes.get('/awsaccounts/{id}/newbucket/')
@action('heaserver-accounts-awsaccount-new-bucket-form')
async def get_new_bucket_form(request: web.Request) -> web.Response:
    """
    Gets form for creating a new bucket in this account.

    :param request: the HTTP request. Required.
    :return: the current bucket, with a template for creating a child folder or Not Found if the requested item does not
    exist.
    ---
    summary: An account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    account_dict, _ = await awsservicelib.get_account_by_id(request)
    return await response.get(request, account_dict)


@routes.post('/awsaccounts/{id}/newbucket')
@routes.post('/awsaccounts/{id}/newbucket/')
async def post_new_bucket(request: web.Request) -> web.Response:
    """
    Gets form for creating a new bucket in this account.

    :param request: the HTTP request. Required.
    :return: the current account, with a template for creating a bucket or Not Found if the requested account does not
    exist.
    ---
    summary: An account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - $ref: '#/components/parameters/id'
    requestBody:
        description: A new bucket.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: Folder example
                  value: {
                    "template": {
                      "data": [
                      {
                        "name": "display_name",
                        "value": "my-bucket"
                      },
                      {
                        "name": "type",
                        "value": "heaobject.bucket.AWSBucket"
                      },
                      {
                        "name": "region",
                        "value": "us-west-1"
                      }]
                    }
                  }
            application/json:
              schema:
                type: object
              examples:
                example:
                  summary: Item example
                  value: {
                    "display_name": "my-bucket",
                    "type": "heaobject.bucket.AWSBucket",
                    "region": "us-west-1"
                  }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.post_bucket(request)


def main() -> None:
    config = init_cmd_line(description='Manages account information details', default_port=8080)
    start(db=aws.S3Manager, wstl_builder_factory=builder_factory(__package__), config=config)
