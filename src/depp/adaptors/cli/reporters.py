from depp.application.ports import reporters


class UpstreamModuleReporter(reporters.Reporter):
    def report(self, module, modules):
        ...


class DownstreamModuleReporter(reporters.Reporter):
    def report(self, module, modules):
        ...
