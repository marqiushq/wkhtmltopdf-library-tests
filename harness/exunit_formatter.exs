# Writes each ExUnit test's result as a line of JSON to $MQ_RESULTS, beside the suite's own
# formatter, which still prints as usual. Loaded from outside the library (elixir -r), so the
# library is not changed; `mix test --trace` would name each test too, but it also turns off
# ExUnit's time limit per test, which the library's own `mix test` keeps.
defmodule LibraryTests.Formatter do
  use GenServer

  def init(opts), do: {:ok, opts}

  def handle_cast({:test_finished, %ExUnit.Test{} = test}, state) do
    {status, message} =
      case test.state do
        nil -> {"passed", ""}
        {:failed, failures} -> {"failed", failures |> Enum.map(&banner/1) |> Enum.join(" / ")}
        {:skipped, reason} -> {"skipped", to_string(reason)}
        {:excluded, reason} -> {"skipped", to_string(reason)}
        {:invalid, _} -> {"failed", "invalid: its module's setup_all failed"}
      end

    line =
      ~s({"name":#{json(to_string(test.name))},"module":#{json(inspect(test.module))},) <>
        ~s("status":#{json(status)},"message":#{json(message)}}\n)

    File.write!(System.fetch_env!("MQ_RESULTS"), line, [:append])
    {:noreply, state}
  end

  def handle_cast(_event, state), do: {:noreply, state}

  defp banner({kind, reason, stack}), do: Exception.format_banner(kind, reason, stack) |> String.slice(0, 400)

  defp json(s) do
    escaped =
      s
      |> String.to_charlist()
      |> Enum.map(fn
        ?" -> ~c"\\\""
        ?\\ -> ~c"\\\\"
        ?\n -> ~c"\\n"
        ?\r -> ~c"\\r"
        ?\t -> ~c"\\t"
        c when c < 32 -> :io_lib.format("\\u~4.16.0B", [c])
        c -> [c]
      end)
      |> List.to_string()

    "\"" <> escaped <> "\""
  end
end
