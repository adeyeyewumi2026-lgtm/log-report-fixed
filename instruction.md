There is an Apache-style access log at /app/access.log. Each line has the form:

<client_ip> - - [<timestamp>] "<METHOD> <path> HTTP/1.1" <status> <bytes>

Parse the file and write a JSON report to /app/report.json (create the file; it does
not exist yet) containing exactly these three keys:

1. "total_requests" (integer) — the number of non-empty lines in /app/access.log.
2. "unique_ips" (integer) — the count of distinct client IPs (the first
   whitespace-delimited field on each line).
3. "top_path" (string) — the request path (the token after the HTTP method inside the
   quoted request, e.g. "/index.html") that appears most often across all requests. If
   there is a tie, any one of the tied paths is accepted.

Do not modify /app/access.log. Write valid JSON with no extra keys.

You have 120 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
