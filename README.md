Content:
<table>
<thead>
<tr>
<th>Module</th>
<th>Algorithm</th>
<th>Variant</th>
</tr>
</thead>
<tbody>
<tr>
<td>Clustering</td>
<td>K-Means</td>
<td>default</td>
</tr>
<tr>
<td rowspan="3">Frequent Itemset</td>
<td rowspan="2">Apriori</td>
<td>default</td>
</tr>
<tr>
<td>hash tree</td>
</tr>
<tr>
<td>Frequent Pattern Tree</td>
<td>default</td>
</tr>
</tbody>
</table>

Project Pages: <https://emankcin.github.io/mining/>

Commands after cloning:
```sh
$ cd mining
$ virtualenv venv
$ . venv/bin/activate
$ pip install pybuilder
$ pyb install_dependencies
$ pyb docs
```

Command to get out of virtual environment:
```sh
$ deactivate
```

Tested on: Ubuntu 16.04 LTS