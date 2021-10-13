export function localeDate(s: string) {
    return new Date(s + "Z").toLocaleString();
}
