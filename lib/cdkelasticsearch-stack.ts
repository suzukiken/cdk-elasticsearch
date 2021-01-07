import * as cdk from "@aws-cdk/core";
import * as es from "@aws-cdk/aws-elasticsearch";
import * as ssm from "@aws-cdk/aws-ssm";

export class CdkelasticsearchStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const DOMAIN_NAME = "cdkelasticsearch";
    const DOMAIN_ARN =
      "arn:aws:es:ap-northeast-1:656169322665:domain/" + DOMAIN_NAME;

    const acm_arn = ssm.StringParameter.fromStringParameterName(
      this,
      "acm_arn",
      "acm-wildcard-figment-research-com-arn"
    ).stringValue;

    const custom_endpoint = ssm.StringParameter.fromStringParameterName(
      this,
      "custom_domain_name",
      "elasticsearch-custom-endpoint"
    ).stringValue;

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

    new cdk.CfnOutput(this, "arn-output", {
      value: domain.attrArn,
      exportName: "cdkelasticsearch-domain-arn",
    });

    new cdk.CfnOutput(this, "endpoint-output", {
      value: domain.attrDomainEndpoint,
      exportName: "cdkelasticsearch-domain-endpoint-host",
    });
  }
}
