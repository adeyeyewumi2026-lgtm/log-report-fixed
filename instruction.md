There is an Apache-style access log at /app/access.log. Each line has the form:

<client_ip> - - [<timestamp>] "<METHOD> <path> HTTP/1.1" <status> <bytes>

Parse the file and write a JSON report to /app/report.json (create the file; it does
not exist yet). Your solution is correct only if all of the following hold:

1. /app/report.json exists and contains valid JSON with exactly these three keys,
   and no others: "total_requests", "unique_ips", "top_path".
2. "total_requests" (integer) equals the number of non-empty lines in
   /app/access.log.
3. "unique_ips" (integer) equals the count of distinct client IPs, where a client
   IP is the first whitespace-delimited field on each line.
4. "top_path" (string) equals the request path (the token after the HTTP method
   inside the quoted request, e.g. "/index.html") that appears most often across
   all requests. If there is a tie, any one of the tied paths is accepted.
5. /app/access.log is left unmodified from its original contents.

You have 120 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
