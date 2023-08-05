# MLPath
A lightweight api for machine and deep learning experiment logging in the form of a python library. 

### Installation
```
pip install mlpath
```

### Get started
import the mlquest module which encompasses all the logging functionality

```Python
from mlpath import mlquest as mlq
l = mlq.l

# let's try this out
def DatasetFilter(x_param, y_param, z_param, **kwargs):
    return x_param * y_param * z_param

def FeatureExtractor(p_num, k_num, l_num, **kwargs):
    return p_num**k_num + l_num

def NaiveBayes(alpha, beta_param, c=0, depth_ratio=4, **kwargs):
    return alpha + beta_param + c


mlq.start('NaiveBayes')

dataset = l(DatasetFilter)(14, 510, 4, m_num=63, g_num=3, h_num=4)
features = l(FeatureExtractor)(12, 2, 12)
accuracy = l(NaiveBayes)(alpha=1024, beta_param=7, c=12,  depth_ratio=538, mega_p=63, g_estim=3, h=43)

mlq.log_metrics(accuracy=accuracy)

mlq.end()
```

Now all your runs are logged in a table likeso:

<table>
<tr>
<th colspan=4 style="text-align: center; vertical-align: middle;">info</th>
<th colspan=6 style="text-align: center; vertical-align: middle;">DatasetFilter</th>
<th colspan=3 style="text-align: center; vertical-align: middle;">FeatureExtractor</th>
<th colspan=7 style="text-align: center; vertical-align: middle;">NaiveBayes</th>
<th colspan=1 style="text-align: center; vertical-align: middle;">metrics</th>
</tr>
<th style="text-align: center; vertical-align: middle;">time</th>
<th style="text-align: center; vertical-align: middle;">date</th>
<th style="text-align: center; vertical-align: middle;">duration</th>
<th style="text-align: center; vertical-align: middle;">id</th>
<th style="text-align: center; vertical-align: middle;">x_param</th>
<th style="text-align: center; vertical-align: middle;">y_param</th>
<th style="text-align: center; vertical-align: middle;">z_param</th>
<th style="text-align: center; vertical-align: middle;">m_num</th>
<th style="text-align: center; vertical-align: middle;">g_num</th>
<th style="text-align: center; vertical-align: middle;">h_num</th>
<th style="text-align: center; vertical-align: middle;">p_num</th>
<th style="text-align: center; vertical-align: middle;">k_num</th>
<th style="text-align: center; vertical-align: middle;">l_num</th>
<th style="text-align: center; vertical-align: middle;">alpha</th>
<th style="text-align: center; vertical-align: middle;">beta_param</th>
<th style="text-align: center; vertical-align: middle;">c</th>
<th style="text-align: center; vertical-align: middle;">depth_ratio</th>
<th style="text-align: center; vertical-align: middle;">mega_p</th>
<th style="text-align: center; vertical-align: middle;">g_estim</th>
<th style="text-align: center; vertical-align: middle;">h</th>
<th style="text-align: center; vertical-align: middle;">accuracy</th>
</tr>
<tr>
<td style="text-align: center; vertical-align: middle;">23:27:13</td>
<td style="text-align: center; vertical-align: middle;">02/07/23</td>
<td style="text-align: center; vertical-align: middle;">0.13 ms</td>
<td style="text-align: center; vertical-align: middle;">1</td>
<td style="text-align: center; vertical-align: middle;">14</td>
<td style="text-align: center; vertical-align: middle;">510</td>
<td style="text-align: center; vertical-align: middle;">4</td>
<td style="text-align: center; vertical-align: middle;">63</td>
<td style="text-align: center; vertical-align: middle;">3</td>
<td style="text-align: center; vertical-align: middle;">4</td>
<td style="text-align: center; vertical-align: middle;">12</td>
<td style="text-align: center; vertical-align: middle;">2</td>
<td style="text-align: center; vertical-align: middle;">12</td>
<td style="text-align: center; vertical-align: middle;">1024</td>
<td style="text-align: center; vertical-align: middle;">7</td>
<td style="text-align: center; vertical-align: middle;">12</td>
<td style="text-align: center; vertical-align: middle;">538</td>
<td style="text-align: center; vertical-align: middle;">63</td>
<td style="text-align: center; vertical-align: middle;">3</td>
<td style="text-align: center; vertical-align: middle;">43</td>
<td style="text-align: center; vertical-align: middle;">1043</td>
</tr>
<tr>
<td style="text-align: center; vertical-align: middle;">23:27:24</td>
<td style="text-align: center; vertical-align: middle;">02/07/23</td>
<td style="text-align: center; vertical-align: middle;">0.12 ms</td>
<td style="text-align: center; vertical-align: middle;">2</td>
<td style="text-align: center; vertical-align: middle;">14</td>
<td style="text-align: center; vertical-align: middle;">510</td>
<td style="text-align: center; vertical-align: middle;">4</td>
<td style="text-align: center; vertical-align: middle;">63</td>
<td style="text-align: center; vertical-align: middle;">3</td>
<td style="text-align: center; vertical-align: middle;">4</td>
<td style="text-align: center; vertical-align: middle;">12</td>
<td style="text-align: center; vertical-align: middle;">2</td>
<td style="text-align: center; vertical-align: middle;">12</td>
<td style="text-align: center; vertical-align: middle;">1024</td>
<td style="text-align: center; vertical-align: middle;">7</td>
<td style="text-align: center; vertical-align: middle;">12</td>
<td style="text-align: center; vertical-align: middle;">538</td>
<td style="text-align: center; vertical-align: middle;">63</td>
<td style="text-align: center; vertical-align: middle;">3</td>
<td style="text-align: center; vertical-align: middle;">43</td>
<td style="text-align: center; vertical-align: middle;">1043</td>
</tr>

such table, the corresponding json and its config file (to filter columns) could be found in the mlquests folder created after the first run.