const std = @import("std");
const print = std.debug.print;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const uri = std.Uri.parse("https://my.sa.ucsb.edu/gold/");

    // http Client
    var client = std.http.Client{ .allocator = allocator };
    defer client.deinit();

    const header_buf: []u8 = try allocator.alloc(u8, 1024 * 2);
    defer allocator.free(header_buf);

    var req = try client.open(.GET, uri, .{ .server_header = header_buf });
    defer req.deinit();

    try req.send();
    try req.finish();
    try req.wait();

    print("Response status: {d}\n\n", .{req.response.status});

    // Print out the headers
    print("{s}\n", .{req.response.iterateHeaders().bytes});

    // Print out the headers (iterate)
    // var it = req.response.iterateHeaders();
    // while (it.next()) |header| {
    //     print("{s}: {s}\n", .{ header.name, header.value });
    // }

    // Read the entire response body, but only allow it to allocate 1024 * 8 of memory.
    const body = try req.reader().readAllAlloc(allocator, 1024 * 8);
    defer allocator.free(body);

    // Print out the body.
    print("{s}", .{body});
}
