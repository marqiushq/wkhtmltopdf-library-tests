// Runs a library's jasmine suite as `npm test` does (its own jasmine, its own spec/support/jasmine.json),
// with one reporter added from here, outside the library, that writes each spec's result as a line
// of JSON to $MQ_RESULTS. The specs are not changed. Run from the library's folder.
var path = require('path');
var fs = require('fs');
var Jasmine = require(path.join(process.cwd(), 'node_modules', 'jasmine'));
var jasmine = new Jasmine({projectBaseDir: process.cwd()});
jasmine.loadConfigFile(path.join(process.cwd(), 'spec', 'support', 'jasmine.json'));
jasmine.addReporter({
  specDone: function (r) {
    var why = (r.failedExpectations || []).map(function (e) { return e.message; }).join(' / ');
    fs.appendFileSync(process.env.MQ_RESULTS, JSON.stringify({name: r.fullName, status: r.status, message: why}) + '\n');
  }
});
jasmine.configureDefaultReporter({});
jasmine.execute();
