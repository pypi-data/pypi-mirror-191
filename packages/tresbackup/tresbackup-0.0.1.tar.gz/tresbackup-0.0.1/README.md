# ES backup tool

CLI for easy ES backup with simple tracking of non-modified indexes

```
usage: Elasticsearch backup [-h] -e es_url [-b batch_size] [-s scroll_time] [-t request_timeout] [-i [indexes ...]] [-x exclude] [-m meta_file] [-f force] [-o output_path]

Makes a backup of all (or specified) indices

optional arguments:
  -h, --help            show this help message and exit
  -e es_url, --es-url es_url
                        Elasticsearch url with url-encoded credentials (if required)
  -b batch_size, --batch-size batch_size
                        Elasticsearch batch size (size) parameter to fetch documents
  -s scroll_time, --scroll-time scroll_time
                        Elasticsearch scroll time parameter to fetch documents
  -t request_timeout, --timeout request_timeout
                        Elasticsearch request timeout in seconds
  -i [indexes ...], --index [indexes ...]
                        Index(es) to backup. If not specified, all indexes are backed up. ES regexes are supported
  -x exclude, --exclude exclude
                        Regular expression to exclude indexes. By default skips all indexes start with '.'
  -m meta_file, --meta-file meta_file
                        Path to metadata file to track indexes changes
  -f force, --force force
                        Ignores exising metadata file and creates backup of all specified indexes
  -o output_path, --output-path output_path
                        Path where backup archives will be stored

```