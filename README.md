# seek-vs-sequential

Seek Vs Seq: A simple demo for two approaches to randomly sampling records 
from a file.  

This is the example code for the Simpsonlab bog post, [On Random vs. Streaming I/O Performance; Or Seek(), and You Shall Find – Eventually](http://simpsonlab.github.io/2015/05/19/io-performance/).  

To run the test on your system:

```
./getdata   # downloads and copies data; ~30GB
./doruns    # takes several hours
Rscript --vanilla plots.R    # uses R for plots
```

Note that most cluster filesystems have very large caches and so the crude trick of reading from separate files isn't enough to get timing data this way.
