# :camera: little brother :camera:
## A non-intrusive, not scary, open source, and simple home-monitoring solution. 

Turn an old phone 📱 into something useful again using Python and OpenCV. 

## What do I need? 

* Old phone (Android or IOS based)
* DroidCam or any other IP camera software
* a LAN (you don't even need internet access, just the router)

## Configuration

Specific things such as the email to send info to, etc. should be specified in the root of the cloned repository,
in a YAML file named __config.yml__. An example is shown below:

```yaml
email: example@gmail.com   # email that you want information sent to by the application
ip: 192.168.0.122:4747      # IP of the droidcam/ip cam instance
framerate: 5                # Framerate of the exported video
```

## References

This project uses openCV's Histogram of Oriented Gradients method to detect humans in its field of view. This paper goes 
into detail on HOG: https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf 



