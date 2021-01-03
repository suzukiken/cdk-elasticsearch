#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { CdkelasticsearchStack } from '../lib/cdkelasticsearch-stack';

const app = new cdk.App();
new CdkelasticsearchStack(app, 'CdkelasticsearchStack');
