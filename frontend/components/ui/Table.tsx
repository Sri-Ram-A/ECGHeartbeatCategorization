"use client";

import React from "react";
import { motion } from "framer-motion";

export type Column<T> = {
  key: string;
  label?: string;
  className?: string;
  render?: (row: T) => React.ReactNode;
};

interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  rowKey: (row: T) => string | number;
  rowClassName?: (row: T, index: number) => string;
}

export function Table<T>({ columns, data, rowKey, rowClassName }: TableProps<T>) {
  return (
    <div className="overflow-hidden rounded-xl border border-gray-800/60 bg-gradient-to-br from-gray-900/70 to-gray-800/40 shadow-xl">
      <table className="w-full text-sm">
        <thead className="bg-gray-900/80 text-gray-400 text-xs uppercase tracking-wider">
          <tr>
            {columns.map((c) => (
              <th key={c.key} className={`p-4 text-left ${c.className ?? ""}`}>
                {c.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <motion.tr
              key={String(rowKey(row))}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.04 }}
              className={`border-t border-gray-800/50 transition-colors hover:bg-blue-900/20 ${rowClassName ? rowClassName(row, i) : ""}`}
            >
              {columns.map((c) => (
                <td key={c.key} className={`p-4 ${c.className ?? ""}`}>
                  {c.render ? c.render(row) : (row as any)[c.key]}
                </td>
              ))}
            </motion.tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Table;

