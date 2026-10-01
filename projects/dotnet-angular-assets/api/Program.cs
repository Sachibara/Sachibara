using Microsoft.EntityFrameworkCore;
var builder = WebApplication.CreateBuilder(args);
Directory.CreateDirectory("data");
builder.Services.AddDbContext<AssetsDb>(options => options.UseSqlite("Data Source=data/assets.db"));
var app = builder.Build();
using (var scope = app.Services.CreateScope()) scope.ServiceProvider.GetRequiredService<AssetsDb>().Database.EnsureCreated();
string? Validate(AssetInput value) {
    if (string.IsNullOrWhiteSpace(value.Tag) || value.Tag.Trim().Length > 40) return "Tag is required (maximum 40 characters).";
    if (string.IsNullOrWhiteSpace(value.Name) || value.Name.Trim().Length > 120) return "Name is required (maximum 120 characters).";
    if (value.Owner is null || value.Owner.Length > 80) return "Owner must be at most 80 characters.";
    if (!new[] {"Available", "Assigned", "Repair", "Retired"}.Contains(value.Status)) return "Invalid asset status.";
    return null;
}
app.MapGet("/api/health", () => Results.Ok(new { status = "ok" }));
app.MapGet("/api/assets", async (AssetsDb db) => await db.Assets.OrderBy(a => a.Tag).ToListAsync());
app.MapGet("/api/assets/{id:int}", async (int id, AssetsDb db) => {
    var asset = await db.Assets.FindAsync(id); return asset is null ? Results.NotFound() : Results.Ok(asset);
});
app.MapPost("/api/assets", async (AssetInput input, AssetsDb db) => {
    var error = Validate(input); if (error is not null) return Results.BadRequest(new { error });
    var tag = input.Tag.Trim().ToUpperInvariant();
    if (await db.Assets.AnyAsync(a => a.Tag == tag)) return Results.Conflict(new { error = "Asset tag already exists." });
    var asset = new Asset { Tag=tag, Name=input.Name.Trim(), Owner=input.Owner.Trim(), Status=input.Status };
    db.Assets.Add(asset);
    try { await db.SaveChangesAsync(); } catch (DbUpdateException) { return Results.Conflict(new { error = "Unable to save; tag may already exist." }); }
    return Results.Created($"/api/assets/{asset.Id}", asset);
});
app.MapPut("/api/assets/{id:int}", async (int id, AssetInput input, AssetsDb db) => {
    var error = Validate(input); if (error is not null) return Results.BadRequest(new { error });
    var asset = await db.Assets.FindAsync(id); if (asset is null) return Results.NotFound();
    var tag = input.Tag.Trim().ToUpperInvariant();
    if (await db.Assets.AnyAsync(a => a.Tag == tag && a.Id != id)) return Results.Conflict(new { error = "Asset tag already exists." });
    asset.Tag=tag; asset.Name=input.Name.Trim(); asset.Owner=input.Owner.Trim(); asset.Status=input.Status;
    try { await db.SaveChangesAsync(); } catch (DbUpdateException) { return Results.Conflict(new { error = "Unable to save; tag may already exist." }); }
    return Results.Ok(asset);
});
app.MapDelete("/api/assets/{id:int}", async (int id, AssetsDb db) => {
    var asset = await db.Assets.FindAsync(id); if (asset is null) return Results.NotFound();
    db.Assets.Remove(asset); await db.SaveChangesAsync(); return Results.NoContent();
});
app.Run();
record AssetInput(string Tag, string Name, string Owner, string Status);
class Asset { public int Id { get; set; } public string Tag { get; set; }=""; public string Name { get; set; }=""; public string Owner { get; set; }=""; public string Status { get; set; }="Available"; }
class AssetsDb(DbContextOptions<AssetsDb> options) : DbContext(options) {
    public DbSet<Asset> Assets => Set<Asset>();
    protected override void OnModelCreating(ModelBuilder model) => model.Entity<Asset>().HasIndex(a => a.Tag).IsUnique();
}
