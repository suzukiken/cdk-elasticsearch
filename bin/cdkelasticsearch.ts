#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { CdkelasticsearchStack } from '../lib/cdkelasticsearch-stack';

const app = new cdk.App();
new CdkelasticsearchStack(app, 'CdkelasticsearchStack', { 
    env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION }
});
