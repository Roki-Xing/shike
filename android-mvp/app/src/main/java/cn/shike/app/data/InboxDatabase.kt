package cn.shike.app.data

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper

private const val DATABASE_NAME = "shike_inbox.db"
private const val DATABASE_VERSION = 1
private const val TABLE_INBOX_ITEMS = "inbox_items"

class InboxDatabase(context: Context) : SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {
    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL(
            """
            CREATE TABLE IF NOT EXISTS $TABLE_INBOX_ITEMS (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                scene TEXT NOT NULL,
                time_text TEXT NOT NULL,
                location TEXT NOT NULL,
                status TEXT NOT NULL,
                source TEXT NOT NULL,
                raw_text TEXT NOT NULL,
                action_labels TEXT NOT NULL,
                start_epoch_millis INTEGER NOT NULL,
                updated_epoch_millis INTEGER NOT NULL,
                archived INTEGER NOT NULL DEFAULT 0
            )
            """.trimIndent(),
        )
        db.execSQL("CREATE INDEX IF NOT EXISTS idx_inbox_items_status ON $TABLE_INBOX_ITEMS(status)")
        db.execSQL("CREATE INDEX IF NOT EXISTS idx_inbox_items_start ON $TABLE_INBOX_ITEMS(start_epoch_millis)")
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        db.execSQL("DROP TABLE IF EXISTS $TABLE_INBOX_ITEMS")
        onCreate(db)
    }
}

fun upsertInboxItem(context: Context, entity: InboxItemEntity) {
    InboxDatabase(context).use { helper ->
        helper.writableDatabase.insertWithOnConflict(
            TABLE_INBOX_ITEMS,
            null,
            entity.toContentValues(),
            SQLiteDatabase.CONFLICT_REPLACE,
        )
    }
}

fun loadInboxHistory(context: Context, limit: Int = 50): List<InboxItemEntity> =
    InboxDatabase(context).use { helper ->
        helper.readableDatabase.query(
            TABLE_INBOX_ITEMS,
            null,
            null,
            null,
            null,
            null,
            "updated_epoch_millis DESC, start_epoch_millis ASC",
            limit.toString(),
        ).use { cursor ->
            buildList {
                while (cursor.moveToNext()) {
                    add(cursor.toInboxItemEntity())
                }
            }
        }
    }

fun clearInboxHistory(context: Context) {
    InboxDatabase(context).use { helper ->
        helper.writableDatabase.delete(TABLE_INBOX_ITEMS, null, null)
    }
}

private fun InboxItemEntity.toContentValues(): ContentValues =
    ContentValues().apply {
        put("id", id)
        put("title", title)
        put("scene", scene)
        put("time_text", time)
        put("location", location)
        put("status", normalizeInboxStatus(status))
        put("source", source)
        put("raw_text", rawText)
        put("action_labels", encodeInboxActions(actionLabels))
        put("start_epoch_millis", startEpochMillis)
        put("updated_epoch_millis", updatedEpochMillis)
        put("archived", if (archived) 1 else 0)
    }

private fun android.database.Cursor.toInboxItemEntity(): InboxItemEntity =
    InboxItemEntity(
        id = getString(getColumnIndexOrThrow("id")),
        title = getString(getColumnIndexOrThrow("title")),
        scene = getString(getColumnIndexOrThrow("scene")),
        time = getString(getColumnIndexOrThrow("time_text")),
        location = getString(getColumnIndexOrThrow("location")),
        status = normalizeInboxStatus(getString(getColumnIndexOrThrow("status"))),
        source = getString(getColumnIndexOrThrow("source")),
        rawText = getString(getColumnIndexOrThrow("raw_text")),
        actionLabels = decodeInboxActions(getString(getColumnIndexOrThrow("action_labels"))),
        startEpochMillis = getLong(getColumnIndexOrThrow("start_epoch_millis")),
        updatedEpochMillis = getLong(getColumnIndexOrThrow("updated_epoch_millis")),
        archived = getInt(getColumnIndexOrThrow("archived")) == 1,
    )
