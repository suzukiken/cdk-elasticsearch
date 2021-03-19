import * as cdk from "@aws-cdk/core";
import * as es from "@aws-cdk/aws-elasticsearch";

export class CdkelasticsearchStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const DOMAIN_NAME = id.toLocaleLowerCase().replace('stack','')
    const acm_arn = 'arn:aws:acm:ap-northeast-1:0000000000:certificate/..............'
    const custom_endpoint = 'elasticsearch.figmentresearch.com'

    const domain = new es.CfnDomain(this, "domain", {
      elasticsearchClusterConfig: { instanceType: "t2.micro.elasticsearch" },
      ebsOptions: { volumeSize: 10, ebsEnabled: true },
      elasticsearchVersion: "2.3",
      domainName: DOMAIN_NAME,
      domainEndpointOptions: {
        enforceHttps: true,
        customEndpoint: custom_endpoint,
        customEndpointCertificateArn: acm_arn,
        customEndpointEnabled: true,
      },

      /*
      accessPolicies: {
        Version: "2012-10-17",
        Statement: [
          {
            Effect: "Allow",
            Principal: {
              AWS: "*",
            },
            Action: "es:ESHttp*",
            Resource: DOMAIN_ARN,
          },
        ],
      },
      */
    });
  }
}
