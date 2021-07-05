+++
title = "CDKでElasticsearch Serviceを起動する方法とインスタンスタイプについて"
date = "2021-03-20"
tags = ["Elasticsearch"]
+++

これは2021年1月ごろの情報です。

### Amplifyの@searchable

AmplifyでGraphQLのスキーマを作るときに@searchable属性をつけると裏側ではElasticsearch Serviceが立ち上がる。

自分はAmplify CLIを使ったバックエンドの作成はしないことにしているので同じようなことをしようと思うと自分でElasticsearch Serviceを立ち上げる必要がある。

なおAmplifyでElasticsearch Serviceが使われる理由はDynamo DBでは全文検索をするコストが高いためだろう。

### バージョンと価格

Elasticsearchにはいくつかのバージョンがあって、本家のElastcではあまり古いバージョンを立ち上げることはできないが、AWSのElasticsearch Serviceはバージョン1.5などの結構古いものが選べる。

この古いバージョンの良いところはインスタンスのタイプが小さいものが選べることでt2.microという選択肢もある。

Amplify CLIで作る場合はもっと新しいバージョンのElasticsearch（6.5とか）になるのだが、この場合インスタンスタイプはt2やt3.smallが必要になると思う。

理由は知らないがドキュメントによるとAmplifyの@searchableはバージョン6.x以上が必要らしい。

https://docs.amplify.aws/cli/graphql-transformer/searchable#known-limitations

> * @searchable is not compatible with Amazon ElasticSearch t2.micro instance as it only works with ElasticSearch version 1.5 and 2.3 and Amplify CLI only supports instances with ElasticSearch version >= 6.x.

でもsmallインスタンスは結構いいお値段なのだ。

[料金 - Amazon Elasticsearch Service | AWS](https://aws.amazon.com/elasticsearch-service/pricing/)

| インスタンスタイプ | 価格/時間   |
|------------------------|----------|
| t2.micro.elasticsearch | $0.028   |
| t2.small.elasticsearch | $0.056   |
| t3.small.elasticsearch | $0.056   |

このうちsmallは最初の1年はFree Tierでほぼ無料で使えると思うので1年間はそれでいいけど、翌年からは毎月数千円、と比較的多めの費用が必要になるだろう。

[料金 - Amazon Elasticsearch Service | AWS](https://aws.amazon.com/elasticsearch-service/pricing/?nc=sn&loc=3)

> You can get started for free on Amazon Elasticsearch Service with the  [AWS Free Tier](https://aws.amazon.com/free/) . For customers in the AWS Free Tier, Amazon Elasticsearch Service provides free usage of up to 750 hours per month of a t2.small.elasticsearch or t3.small.elasticsearch instance and 10GB per month of optional EBS storage (Magnetic or General Purpose).

他の方法として考えられるのは例えばElastic.coを使うというもので、しかしAWSに載せる形でインスタンスを立ち上げてみると、そこそこの費用にはなるわけで、どうせならAWSで構築してCDKで管理できる方が楽というのもある。

その他AWSは、ユーザーが自分でインスタンスを立てられるようにOpen DistroのAMIを用意していてそれを使う手もあるかと思ったが、最低2GBのメモリのインスタンスを選ぶように書かれていて、それは結局安いものではない。しかもアマゾンのマネージドサービスがいいので、あんまり使いたいものでもない。

[Amazon Machine Image - Open Distro for Elasticsearch Documentation](https://opendistro.github.io/for-elasticsearch-docs/docs/install/ami/)

>  Choose an instance type with at least 2 GiB of RAM


### 結局

結局調べた範囲では、安めに済ませるプランならこうなる。

| 項目 | 値   |
|------------------------|----------|
| Elasticsearchバージョン | 2.3   |
| インスタンスタイプ | t2.micro.elasticsearch   |
| 月額 | 20 USD（アバウト）   |

ちなみにこれがAmplifyで利用できないわけではなくて、例えばGraphQLでAppSync経由でElasticsearch Serviceのバージョン2.3のインスタンスを使うことはできる。というか簡単に試す範囲ではできた。つまり必ずしもAmplifyのバックエンドが6.x以降でないとダメということではない。

機能としては2.3ではできないクエリなどもあると思うがやりたいことはできるし、安価に済ませるならそれで良いのではという気はする。

## CDKのコード

サンプルの[Githubのリポジトリ](https://github.com/suzukiken/cdkelasticsearch)

https://elasticsearch.figmentresearch.comで起動する。アクセス権限の設定はこれを利用するLambdaやAppSync側のロールで指定する。

テストのためにデータを投入しやすいようにするならaccessPoliciesのところで自分のアカウントから全アクセスを可能にするとかできる。あまりにも自由な設定にすると`cdk deploy`時に`Apply a restrictive access policy to your domain`と言われてデプロイできない。

### と言いつつElasticsearch Serviceは使わないことにしている

ただ自分の場合は、というか自分が作ろうと思っているものの範囲では、Elasticsearch Serviceは運用コストがかかりすぎるので検索はAthenaで行うことにした。

だから結局Elasticsearch Serviceは使っていないし、使うつもりもないのだが、以前調べたことを忘れないうちに残しておこうということでこの記事を書いた。
