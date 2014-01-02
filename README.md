dodgy
=====

Dodgy is a very basic tool to run against your codebase to search for "dodgy" looking values. It is a series of simple regular expressions designed to detect things such as accidental SCM diff checkins, or passwords or secret keys hard coded into files.

While this is primarily aimed at open source projects (for whom a publicly available secret key is pretty dangerous), it can also be used in private projects, with the caveat that it will point out things which are not a problem for private projects and is not configurable enough currently to change that.

Another note - this tool is probably best run pre-commit, since it will hopefully prevent dodgy things being checked in.


Status
---

[![Latest Version](https://pypip.in/v/dodgy/badge.png)](https://crate.io/packages/dodgy)
[![Build Status](https://travis-ci.org/landscapeio/dodgy.png?branch=master)](https://travis-ci.org/landscapeio/dodgy) 
[![Code Health](https://landscape.io/github/landscapeio/dodgy/master/landscape.png)](https://landscape.io/github/landscapeio/dodgy/master)
[![Coverage Status](https://coveralls.io/repos/landscapeio/dodgy/badge.png)](https://coveralls.io/r/landscapeio/dodgy)

This is a very early version with minimal functionality right now, but will be improved over time. 

It was written as one of several tools for [landscape.io](https://landscape.io), a code metrics and repository analyser for Python. As such, the features will mostly reflect the needs of Landscape in the early stages.
