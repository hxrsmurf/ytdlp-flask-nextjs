# Background

My setup:
- Xfinity internet 
  - 1 Gbps download and 20 Mbps upload
  - *great* 1 TiB bandwidth cap per month  
- Gaming Rig
   - I don't keep this online all the time
   - GTX 1080 & Ryzen 7 2700x
- Intel NUC
  - I keep this online all the time
  -  16 GiB RAM, i3-5010U

I want to be able to:

1. Download YouTube video (MP4)
2. Convert to HLS with `ffmpeg`
3. Serve on website

The NUC struggles with HLS conversion and I don't leave my gaming rig on all the time. 

While I'm all about self-hosting, the NUC struggles with HLS conversion and I don't leave my gaming rig on all the time (maybe I will).

So, I'm wanting to pursue different methods for this.

I currently use BackBlaze, DigitalOcean, and CloudFlare. So, I opted to try those first.


# BackBlaze B2
I've had my data with them for years. $0.005/GiB per month. Hard to beat. And thrown a CDN in front that participates in BandWidth Alliance...golden!

# CloudFlare
Since CloudFlare and BackBlaze are in the `Bandwidth Alliance` and I'm familar with both of them, I started with this. CloudFlare is currently serving the files directly from the BackBlaze bucket.

CloudFlare stream is $5/month. I'm not sure what specific additional charges there are, but that seems pretty good.

As far as I can tell/find, the bandwidth for CloudFlare is free.

# DigitalOcean
DigitalOcean pricing is an hour minimum. Right now I don't have a good way to predict how long a video would take to encode. So it'd be difficult to optimize that hour. Whether it be an hour-long video or multiple, smaller videos with a backend queue to queue 'em up. So, unfortunately, their out for HLS processing. However, the basic download/upload they'd be great since each Droplet has bandwidth!

I haven't checked out their $5/month Spaces yet, but its only 250 GiB and B2 is much cheaper.


# BunnyCDN
I forget where I heard of BunnyCDN, but so far I'm liking them. Their storage is $0.02/GB per month and encoding is free. I've got a few files uploaded to them and I figured out their APIs. 

They seem to be good solution for encoding (since it's free). And the storage is a good price. I've got to look a how much their CDN is to serve the videos.

# AWS

On 7/30/2022, I spent a few hours running tests. I have some more notes/thoughts [here](https://github.com/hxrsmurf/ytdlp-flask-nextjs/blob/master/aws/ReadMe.md)

The t2.micro was fine for `yt-dlp` and `curl` to BunnyCDN and I'm sure to CloudFlare.

For HLS Converting with `ffmpeg`, I tested with a few instance types:

- t2 (not sure why I didn't test this)
- t3
- m5
- c4
- c5

Looking at the cost per minute the server was online ffmpeg-ing (cost effectiveness)

16 vCPU
- c4/c5 4x.large

8 vCPU
- c4.2xlarge - At first, I didn't believe this was true...but I ran a few tests and something with this instance type is just dirt slow.
- t3.2xlarge - This performed pretty well

I'd opt for the c5.4xlarge for me personally. Its cost effectiveness and quickness is great!

With all that said, the extraordinary cost of AWS/Azure/GCP egress bandwidth is $0.09/GB after the first 100 GB. That's a lot.

So, I'd be **forced** to use their CDN or *not* do HLS conversions.



| CPU | Memory | Type        | FFMPEG Rate | Price  | Per Minute | Video Length | Minutes Taken | Cost Server |
| --- | ------ | ----------- | ----------- | ------ | ---------- | ------------ | ------------- | ----------- |
| 36  | 60     | c4.8xlarge  | 1.38        | 0.5449 | 0.0091     | 90.00        | 65.22         | 0.592283    |
| 36  | 72     | c5.9xlarge  | 3.10        | 0.6739 | 0.0112     | 90.00        | 29.03         | 0.326081    |
| 8   | 15     | c4.2xlarge  | 0.95        | 0.1825 | 0.0030     | 90.00        | 94.74         | 0.288158    |
| 4   | 7.5    | c4.xlarge   | 0.46        | 0.0694 | 0.0012     | 90.00        | 195.65        | 0.226304    |
| 2   | 8      | m5.large    | 0.25        | 0.0362 | 0.0006     | 90.00        | 360.00        | 0.217200    |
| 16  | 30     | c4.4xlarge  | 1.75        | 0.2486 | 0.0041     | 90.00        | 51.43         | 0.213086    |
| 8   | 32     | t3a.2xlarge | 0.66        | 0.0902 | 0.0015     | 90.00        | 136.36        | 0.205000    |
| 16  | 32     | c5.4xlarge  | 2.20        | 0.2641 | 0.0044     | 90.00        | 40.91         | 0.180068    |
| 2   | 3.75   | c4.large    | 0.26        | 0.0308 | 0.0005     | 90.00        | 346.00        | 0.177613    |
| 2   | 4      | c5.large    | 0.30        | 0.0354 | 0.0006     | 90.00        | 300.00        | 0.177000    |
| 8   | 32     | t3.2xlarge  | 0.85        | 0.0998 | 0.0017     | 90.00        | 105.88        | 0.176118    |
| 4   | 16     | t3.xlarge   | 0.45        | 0.0499 | 0.0008     | 90.00        | 200.00        | 0.166333    |
| 2   | 8      | t3.large    | 0.25        | 0.0265 | 0.0004     | 90.00        | 360.00        | 0.159000    |
| 2   | 4      | t3.medium   | 0.24        | 0.0125 | 0.0002     | 90.00        | 375.00        | 0.078125    |